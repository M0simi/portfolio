import os
from io import BytesIO
from typing import Tuple

import google.generativeai as genai
from PyPDF2 import PdfReader

from django.core.files.storage import default_storage  # للاحتياط
from core.models import KnowledgeBase


# =======================
# إعداد Gemini
# =======================
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


def _open_file_bytes_from_field(file_field) -> bytes:
    """
    يقرأ بايتات الملف من الـ storage المرتبط بالحقل نفسه.
    لا يستخدم أي URL عام – هذا يتجنب 401 من Cloudinary.
    """
    # أفضل طريقة: نستخدم storage الخاص بالحقل
    storage = getattr(file_field, "storage", None)
    name = getattr(file_field, "name", None)

    if storage and name:
        with storage.open(name, "rb") as f:
            return f.read()

    # احتياط (حالات نادرة): لو ما قدرنا نستخدم storage الخاص بالحقل
    # نجرّب default_storage بنفس الاسم
    if name:
        with default_storage.open(name, "rb") as f:
            return f.read()

    raise RuntimeError("تعذّر تحديد موضع الملف لقراءته (لا storage ولا name).")


def _extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    يستخرج نصًا من ملف PDF (بايتات).
    """
    reader = PdfReader(BytesIO(pdf_bytes))
    parts = []
    for p in reader.pages:
        try:
            t = p.extract_text() or ""
            if t:
                parts.append(t)
        except Exception:
            # نتجاوز أي صفحة تسبّب خطأ
            continue
    return "\n".join(parts).strip()


def _load_latest_kb_text() -> Tuple[str, str]:
    """
    يرجع (title, text) لآخر عنصر بقاعدة المعرفة.
    لو فيه field نصّي مستقبلاً بنستعمله؛ الآن نعتمد على PDF.
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb or not kb.file:
        raise RuntimeError("لا يوجد ملف قاعدة معرفة مرفوع بعد.")

    pdf_bytes = _open_file_bytes_from_field(kb.file)
    text = _extract_text_from_pdf_bytes(pdf_bytes)
    if not text:
        raise RuntimeError("تعذّر استخراج نصوص من ملف PDF.")

    return kb.title or "Knowledge Base", text


def ask_gemini(user_prompt: str) -> str:
    """
    يجيب على سؤال المستخدم مع تقييد الإجابة بما هو موجود في PDF فقط.
    """
    if not API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    try:
        kb_title, kb_text = _load_latest_kb_text()
    except Exception as e:
        # نُظهر السبب للمستخدم أثناء الاختبار
        return f"⚠️ تعذّر فتح/قراءة ملف المعرفة: {e}"

    system_rule = (
        "أنت UniBot 🎓 — مساعد جامعي يجيب بالعربية الفصحى،"
        " وتعتمد إجابتك فقط على النص التالي من دليل الجامعة. "
        "إذا لم تجد الإجابة في النص، قل: "
        "«عذرًا، سؤالك غير موجود في الملف الحالي.»"
    )

    prompt = (
        f"{system_rule}\n\n"
        f"--- مقتطف من ({kb_title}) ---\n"
        f"{kb_text[:6000]}\n"
        f"--- نهاية المقتطف ---\n\n"
        f"سؤال المستخدم:\n{user_prompt}\n"
    )

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        if not text.strip():
            return "عذرًا، سؤالك غير موجود في الملف الحالي."
        # تنظيف بسيط
        text = (
            text.replace("حسب الملف", "")
                .replace("وفقًا للمستند", "")
                .replace("PDF", "")
                .replace("الملف", "")
                .strip()
        )
        if not text:
            return "عذرًا، سؤالك غير موجود في الملف الحالي."
        return text
    except Exception as e:
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {e}"
