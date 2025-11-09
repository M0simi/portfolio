# core/ai_service.py
import os
from io import BytesIO
from typing import Optional

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
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# إعدادات الأمان: تعطيل الحجب (مفيد لأسئلة “الحرمان” وما شابه)
safety_settings = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH:      HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT:       HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# حدود لأداء أفضل
MAX_CHARS  = 60_000
MAX_PAGES  = 40        # لا نقرأ أكثر من 40 صفحة
REQ_TIMEOUT = 25       # ثوانٍ


def _download_via_url(url: str) -> bytes:
    """ينزّل الملف من رابط عام (Cloudinary raw) بطريقة متسامحة."""
    headers = {
        "User-Agent": "UniBot/1.0 (+https://unibot.foo)"
    }
    resp = requests.get(url, headers=headers, timeout=REQ_TIMEOUT, allow_redirects=True)
    # بعض ردود Cloudinary تكون 200 مع رسائل JSON داخل الصفحة إذا العارض الداخلي فشل،
    # لكن الرابط raw عادة يرجع PDF صحيح.
    resp.raise_for_status()

    # فحص مبدئي للمحتوى (لا نوقف لو ما كان مضبوط 100%)
    ctype = resp.headers.get("Content-Type", "").lower()
    if "pdf" not in ctype and not url.lower().endswith(".pdf"):
        # مو شرط نوقف — بس ننبّه عن نوع غريب
        pass

    return resp.content


def _open_via_storage(name: str) -> bytes:
    """مسار احتياطي عند التطوير محلياً أو تخزين محلي."""
    with default_storage.open(name, "rb") as fh:
        return fh.read()


def _extract_pdf_text(pdf_bytes: bytes, max_pages: int = MAX_PAGES, max_chars: int = MAX_CHARS) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    parts = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t:
            parts.append(t)
        if sum(len(x) for x in parts) >= max_chars:
            break
    return ("\n".join(parts))[:max_chars].strip()


def _read_latest_kb_text() -> str:
    """
    يقرأ أحدث دليل/FAQ:
    1) من الرابط العام (Cloudinary raw) — المسار الأساسي
    2) من التخزين (احتياطي)، مفيد محليًا
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # لو عندك حقل نصّي، نستخدمه مباشرة
    inline = (getattr(kb, "content", "") or "").strip()
    if inline:
        return inline[:MAX_CHARS]

    f = getattr(kb, "file", None)
    if not f:
        return ""

    # نحاول بالرابط العام أولاً
    last_err: Optional[Exception] = None
    file_url = getattr(f, "url", "") or ""
    if file_url:
        try:
            data = _download_via_url(file_url)
            return _extract_pdf_text(data)
        except Exception as e:
            last_err = e  # ندوّن الخطأ ونكمّل بالمسار الاحتياطي

    # احتياطي: التخزين (محلي/ديف)
    try:
        data = _open_via_storage(f.name)
        return _extract_pdf_text(data)
    except Exception as e:
        # أعطي رسالة واضحة فيها السبب الأول إن وجد
        reason = f"{last_err}" if last_err else f"{e}"
        raise RuntimeError(f"تعذّر فتح/قراءة ملف المعرفة: {reason}")


def ask_gemini(user_prompt: str) -> str:
    """يولّد إجابة بالاستناد إلى أحدث دليل/FAQ مرفوع."""
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    try:
        kb_text = _read_latest_kb_text()
    except Exception as e:
        return f"⚠️ خطأ في الإعداد أو قراءة الملف: {e}"

    system_rule = (
        "أنت UniBot 🎓، المساعد الذكي الرسمي لجامعتنا. "
        "قدّم إجابات دقيقة ومهذبة بالعربية الفصحى اعتمادًا حصريًا على نص الدليل أدناه. "
        "إن لم تجد الإجابة في النص، قل: "
        "«عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة.»"
    )

    prompt = f"""{system_rule}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

    # جرّب النموذج المضبوط بيئياً ثم الرجوع الافتراضي
    model_candidates = [MODEL_NAME, "gemini-1.5-flash"]
    last_err = None

    for name in model_candidates:
        try:
            model = genai.GenerativeModel(name, safety_settings=safety_settings)
            resp = model.generate_content(prompt)

            # أحيانًا تُحجب الإجابة (ليس الطلب) — نعالجها بلطف
            if not getattr(resp, "candidates", None):
                return "عذرًا، تم حظر الرد لأسباب تتعلق بالأمان. حاول إعادة صياغة السؤال."

            text = (getattr(resp, "text", "") or "").strip()
            if not text:
                text = ("عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. "
                        "للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة.")
            return text
        except Exception as e:
            last_err = e
            continue

    return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err}"
