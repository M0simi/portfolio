import os
from io import BytesIO

from django.core.files.storage import default_storage
from core.models import KnowledgeBase
from PyPDF2 import PdfReader

import google.generativeai as genai

# ----------------------------------
# إعداد Gemini
# ----------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


def _read_latest_kb_bytes():
    """
    يقرأ أحدث محتوى من قاعدة المعرفة:
    - إن وجد content نصّي يُعاد كنص.
    - إن وجد ملف PDF يُقرأ بايتات عبر default_storage.open(...)
      (يعمل مع Cloudinary بدون الحاجة لرابط عام).
    - عند الفشل يرجع (None, رسالة خطأ).
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return None, "⚠️ لا يوجد ملف/محتوى في قاعدة المعرفة."

    # محتوى نصّي مباشر؟
    content = (getattr(kb, "content", "") or "").strip()
    if content:
        return content.encode("utf-8"), None

    # ملف؟
    f = getattr(kb, "file", None)
    if not f:
        return None, "⚠️ لا يوجد ملف مرفوع في قاعدة المعرفة."

    # القراءة عبر التخزين (يدعم Cloudinary/private)
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
        return data, None
    except Exception as e:
        # لا نستخدم f.url لتجنب 401
        return None, f"⚠️ تعذّر فتح الملف من التخزين: {e}"


def _pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    """
    يحوّل PDF (بايتات) إلى نص.
    """
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        parts = []
        for p in reader.pages:
            try:
                t = p.extract_text() or ""
                if t:
                    parts.append(t)
            except Exception:
                continue
        return "\n".join(parts).strip()
    except Exception as e:
        return f"⚠️ خطأ أثناء قراءة ملف PDF: {e}"


def ask_gemini(user_prompt: str) -> str:
    """
    يبني برومبت مع محتوى الدليل ويرسل إلى Gemini ويعيد النص.
    يرجّع رسالة عربية واضحة عند أي خطأ بدلاً من رفع استثناءات.
    """
    if not API_KEY:
        return "❌ لم يتم تعيين مفتاح GEMINI_API_KEY."

    kb_bytes, err = _read_latest_kb_bytes()
    if err:
        return err

    # إن كانت bytes (PDF) حوّلها لنص، وإن كانت أصلاً نص (جاي من content) نستخدمه كما هو
    if isinstance(kb_bytes, (bytes, bytearray)):
        base_text = _pdf_bytes_to_text(kb_bytes)
        if base_text.startswith("⚠️"):
            return base_text
    else:
        base_text = str(kb_bytes or "")

    if not base_text.strip():
        return "⚠️ تعذّر استخراج نصوص من الدليل."

    full_prompt = f"""
أنت UniBot 🎓 — مساعد جامعي ذكي بالعربية الفصحى.
أجب فقط من النص التالي المقتبس من دليل الجامعة. إن لم تجد الإجابة فيه فقل:
"عذرًا، سؤالك غير موجود في الملف الحالي."

--- نص الدليل (مقتطف حتى 6000 حرف) ---
{base_text[:6000]}

--- سؤال المستخدم ---
{user_prompt}
"""

    try:
        model = genai.GenerativeModel(MODEL_ID)
        resp = model.generate_content(full_prompt)
        text = getattr(resp, "text", "") or ""
        text = text.strip()
        if not text:
            return "❌ لم يصلني رد من خدمة Gemini."
        # تنظيف بسيط
        for bad in ("حسب الملف", "وفقًا للمستند", "PDF", "الملف"):
            text = text.replace(bad, "")
        text = text.strip()
        if not text:
            text = "عذرًا، سؤالك غير موجود في الملف الحالي."
        return text
    except Exception as e:
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {e}"
