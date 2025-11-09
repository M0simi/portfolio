# core/ai_service.py
import os
from io import BytesIO

import requests
import google.generativeai as genai
from google.generativeai.types import SafetySetting, HarmCategory, HarmBlockThreshold

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase


# =======================
# إعداد Gemini
# =======================
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()

# اسم الموديل من البيئة مع حراسة للأسماء الخاطئة/القديمة
def _resolve_model_name() -> str:
    env_name = (os.getenv("GEMINI_MODEL") or "").strip().lower()
    if env_name in ("gemini-1.5-flash", "gemini-1.5-flash-latest", "flash"):
        return "gemini-1.5-flash-latest"
    if env_name in ("gemini-1.5-pro", "gemini-1.5-pro-latest", "pro"):
        return "gemini-1.5-pro-latest"
    # fallback آمن
    return "gemini-1.5-flash-latest"

MODEL_NAME = _resolve_model_name()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# تعطيل الفلاتر (السماح الكامل)
SAFETY_SETTINGS = [
    SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,        threshold=HarmBlockThreshold.BLOCK_NONE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT,         threshold=HarmBlockThreshold.BLOCK_NONE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,  threshold=HarmBlockThreshold.BLOCK_NONE),
]


def _read_latest_kb_text(max_chars: int = 60_000) -> str:
    """
    يقرأ أحدث محتوى معرفة:
      1) إن وُجد نص مباشر في الحقل content يُستخدم أولاً.
      2) خلاف ذلك يُقرأ ملف PDF من التخزين الافتراضي (محلي/Cloudinary).
         - لو التخزين لا يدعم .path، نستخدم public URL وننزّل الملف عبر requests.
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # نص مباشر إن توفر
    content_text = (getattr(kb, "content", "") or "").strip()
    if content_text:
        return content_text[:max_chars]

    # ملف إن توفر
    f = getattr(kb, "file", None)
    if not f:
        return ""

    data: bytes | None = None

    # محاولة القراءة عبر التخزين الافتراضي (سيعمل مع التخزين المحلي)
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
    except Exception:
        data = None

    # في حال فشل التخزين (Cloudinary raw) نستخدم الرابط العام
    if data is None:
        file_url = getattr(f, "url", None)
        if not file_url:
            return ""
        try:
            # نسمح بإعادة التوجيه ونزيد مهلة معقولة
            resp = requests.get(file_url, allow_redirects=True, timeout=30)
            resp.raise_for_status()
            data = resp.content
        except Exception:
            return ""

    # محاولة استخراج النص من PDF
    try:
        reader = PdfReader(BytesIO(data))
        parts: list[str] = []
        total = 0
        for p in reader.pages:
            try:
                t = p.extract_text() or ""
            except Exception:
                t = ""
            if t:
                parts.append(t)
                total += len(t)
                if total >= max_chars:
                    break
        return ("\n".join(parts))[:max_chars].strip()
    except Exception:
        # إذا الملف ليس PDF أو فشل الاستخراج، نرجع فارغ
        return ""


def ask_gemini(user_prompt: str) -> str:
    """
    يُولّد إجابة اعتماداً على أحدث دليل/FAQ:
      - يدمج مقتطفاً من قاعدة المعرفة في الـ prompt.
      - يستخدم google-generativeai>=0.8.3 (واجهة v1).
      - يُعطل فلاتر السلامة.
    """
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    kb_text = _read_latest_kb_text()

    system_rule = (
        "أنت UniBot 🎓، المساعد الذكي الرسمي للجامعة. "
        "أجب باللغة العربية الفصحى فقط، وباختصار ووضوح. "
        "اعتمد حصراً على المعلومات الواردة في دليل الجامعة أدناه. "
        "لا تختلق معلومات غير موجودة. "
        "إن لم تجد إجابة في النص، قل: "
        "«عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة.»"
    )

    prompt = f"""{system_rule}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

    # نجرب أولاً الاسم المحسوم، وإن فشل نُسقِط على flash-latest كنسخة احتياط
    candidates = [MODEL_NAME, "gemini-1.5-flash-latest"]
    last_err: Exception | None = None

    for name in candidates:
        try:
            model = genai.GenerativeModel(name=name, safety_settings=SAFETY_SETTINGS)
            resp = model.generate_content(prompt)

            # تحقُّق أساسي
            text = (getattr(resp, "text", "") or "").strip()
            if not text:
                text = (
                    "عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. "
                    "للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة."
                )
            return text
        except Exception as e:
            last_err = e
            continue

    return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err!s}"
