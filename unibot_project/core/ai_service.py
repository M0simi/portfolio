import os
from io import BytesIO
import requests

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase

# =======================
# إعداد Gemini
# =======================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ENV_MODEL = os.getenv("GEMINI_MODEL", "").strip()  # مثال: gemini-1.5-flash-latest

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# تعطيل فلاتر الحجب (القيم الصحيحة)
safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH:      HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT:       HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

def _read_latest_kb_text(max_chars: int = 60_000) -> str:
    """
    يقرأ أحدث ملف/محتوى من قاعدة المعرفة.
    - إن وجد نص content يستخدمه.
    - وإلا ينزّل PDF من رابط Cloudinary العام ثم يستخرج النص.
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # لو عندك حقل نصّي في الموديل
    content_text = (getattr(kb, "content", "") or "").strip()
    if content_text:
        return content_text[:max_chars]

    f = getattr(kb, "file", None)
    if not f:
        return ""

    # جرّب عبر التخزين أولاً (لو محلي)
    data = None
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
    except Exception:
        data = None

    # لو ما نفع، حمّل من الرابط العام ل Cloudinary
    if data is None:
        file_url = getattr(f, "url", None)
        if not file_url:
            raise RuntimeError("الملف موجود لكن لا يملك رابط URL عام.")
        r = requests.get(file_url, timeout=20)
        r.raise_for_status()
        data = r.content

    reader = PdfReader(BytesIO(data))
    parts = []
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

def ask_gemini(user_prompt: str) -> str:
    """يولّد إجابة بالاستناد إلى أحدث دليل/FAQ مرفوع."""
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    try:
        kb_text = _read_latest_kb_text()

        # قائمة موديلات بديلة — الجرّاح يجرّب المتاح تلقائيًا
        model_candidates = [
            ENV_MODEL or "gemini-1.5-flash-latest",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro-latest",
            "gemini-1.5-pro",
        ]

        system_rule = (
            "أنت UniBot 🎓، المساعد الذكي الرسمي للجامعة. "
            "أجب باللغة العربية الفصحى فقط، وبناءً على نص الدليل التالي. "
            "إن لم تجد الإجابة في النص، قل بأدب: "
            "«عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي.»"
        )

        prompt = f"""{system_rule}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

        last_err = None
        for name in model_candidates:
            try:
                model = genai.GenerativeModel(model_name=name, safety_settings=safety_settings)
                resp = model.generate_content(prompt)

                # في بعض الحالات قد لا يعيد نص مباشرة
                text = (getattr(resp, "text", "") or "").strip()
                if not text and getattr(resp, "candidates", None):
                    parts = []
                    for c in resp.candidates:
                        ct = getattr(c, "content", None)
                        if ct and getattr(ct, "parts", None):
                            for prt in ct.parts:
                                val = getattr(prt, "text", "") or ""
                                if val:
                                    parts.append(val)
                    text = "\n".join(parts).strip()

                if not text:
                    text = "عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي."

                return text

            except Exception as e:
                last_err = e
                continue

        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err}"

    except Exception as e:
        return f"⚠️ خطأ في الإعداد أو قراءة الملف: {e}"
