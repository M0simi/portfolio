import os
from io import BytesIO

import google.generativeai as genai
from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase  # عدّل المسار حسب مشروعك

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest").strip()  # بدّلها لو حاب

def _read_latest_kb_text(max_chars: int = 60_000) -> str:
    """يقرأ أحدث ملف/محتوى من قاعدة المعرفة عبر التخزين المعرّف (Cloudinary أو محلي)."""
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # لو عندك حقل نصّي إضافي (مثل content) استخدمه أولاً
    text = (getattr(kb, "content", "") or "").strip()
    if text:
        return text[:max_chars]

    # FileField (resource_type=raw في Cloudinary)
    f = getattr(kb, "file", None)
    if not f:
        return ""

    # نقرأ عبر default_storage عشان ما نعتمد على روابط عامة
    with default_storage.open(f.name, "rb") as fh:
        data = fh.read()

    reader = PdfReader(BytesIO(data))
    parts = []
    for p in reader.pages:
        try:
            t = p.extract_text() or ""
        except Exception:
            t = ""
        if t:
            parts.append(t)
        if sum(len(x) for x in parts) >= max_chars:
            break

    return ("\n".join(parts))[:max_chars].strip()

def ask_gemini(user_prompt: str) -> str:
    """يولّد إجابة بالاستناد إلى أحدث دليل/FAQ مرفوع."""
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    genai.configure(api_key=GEMINI_API_KEY)

    # جرّب أولاً الموديل الافتراضي، ولو فشل غيّره إلى الاسم الثابت دون -latest
    model_names = [MODEL_NAME, "gemini-1.5-flash", "gemini-1.5-pro"]  # fallback
    kb_text = _read_latest_kb_text()

    system_preamble = (
        "أنت UniBot 🎓 — مساعد جامعي عربي فصيح. "
        "اعتمد فقط على النص المزود. إن لم تجد الجواب، قل: "
        "«عذرًا، سؤالك غير موجود في الملف الحالي.»"
    )

    prompt = f"""{system_preamble}

--- مقتطف من الدليل/الأسئلة (قد يكون مختصراً) ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

    last_err = None
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            resp = model.generate_content(prompt)
            text = getattr(resp, "text", "") or ""
            text = text.strip()
            if not text:
                text = "عذرًا، سؤالك غير موجود في الملف الحالي."
            return text
        except Exception as e:
            last_err = e
            continue

    return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err}"
