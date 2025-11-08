# core/ai_service.py
from __future__ import annotations

import os
from io import BytesIO

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

import google.generativeai as genai
from core.models import KnowledgeBase


# =========================
# إعداد مفاتيح Gemini
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# تقدر تغيّر الموديل من env، الافتراضي ممتاز للاستجابة السريعة
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def _ensure_gemini_configured() -> str | None:
    """
    يتحقق أن مفتاح Gemini موجود ويهيّئ المكتبة.
    يرجّع None إذا كل شيء تمام، أو رسالة خطأ إن كان فيه نقص.
    """
    if not GEMINI_API_KEY:
        return "❌ لم يتم العثور على المفتاح GEMINI_API_KEY في المتغيرات."
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        return f"⚠️ تعذّر تهيئة Gemini: {e}"
    return None


# =========================
# قراءة أحدث ملف PDF مرفوع
# =========================
def _load_latest_pdf_text() -> str:
    """
    يقرأ نص آخر ملف PDF من نموذج KnowledgeBase عبر واجهة التخزين
    (تعمل على التخزين المحلي وCloudinary بنفس الأسلوب).
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb or not getattr(kb, "file", None):
        return "❌ لا يوجد ملف مرفوع في قاعدة المعرفة."

    file_name = getattr(kb.file, "name", None)
    if not file_name:
        return "❌ لا يمكن تحديد اسم الملف المرفوع."

    try:
        with default_storage.open(file_name, "rb") as f:
            pdf_bytes = f.read()
    except Exception as e:
        return f"⚠️ خطأ أثناء فتح الملف من التخزين: {e}"

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        pages = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            if txt:
                pages.append(txt)
        text = "\n".join(pages).strip()
        if not text:
            return "⚠️ لم أستطع استخراج نص من ملف الـ PDF."
        return text
    except Exception as e:
        return f"⚠️ خطأ أثناء قراءة/استخراج نص PDF: {e}"


# =========================
# دالة سؤال Gemini
# =========================
def ask_gemini(user_prompt: str) -> str:
    """
    يجيب من Gemini اعتمادًا على نص ملف الـ PDF فقط.
    لو ما لقي معلومة، يرجّع رسالة اعتذار ثابتة.
    """
    # 1) تأكد من المفتاح
    err = _ensure_gemini_configured()
    if err:
        return err

    # 2) اقرأ نص الـ PDF
    pdf_text = _load_latest_pdf_text()
    if pdf_text.startswith(("❌", "⚠️")):
        return pdf_text

    # 3) جهّز البرومبت (نقصّ النص إذا كان طويل)
    context_chunk = pdf_text[:6000]
    full_prompt = f"""
أنت UniBot 🎓 — مساعد جامعي يجيب بالعربية الفصحى.
أجب اعتمادًا فقط على النص التالي المقتبس من دليل الجامعة.
إذا لم تجد إجابة مباشرة في النص، قل حرفيًا:
"عذرًا، سؤالك غير موجود في الملف الحالي."

🔹 نص الدليل (مسموح لك بالاعتماد عليه فقط):
{context_chunk}

🔹 سؤال المستخدم:
{user_prompt}
""".strip()

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        resp = model.generate_content(full_prompt)

        # حالات السلامة (Safety) أحيانًا تمنع الرد
        if hasattr(resp, "prompt_feedback") and resp.prompt_feedback:
            # نعرض سبب المنع باختصار إن وجد
            reason = getattr(resp.prompt_feedback, "block_reason", None)
            if reason:
                return f"⚠️ تعذّر توليد إجابة (Safety: {reason})."

        text = (getattr(resp, "text", None) or "").strip()
        if not text:
            return "❌ لم يتم العثور على رد."
        # تنظيف بسيط
        if "غير موجود في الملف" in text or "لا أجد" in text:
            return "عذرًا، سؤالك غير موجود في الملف الحالي."
        return text
    except Exception as e:
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {e}"

