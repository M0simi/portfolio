import os
from io import BytesIO
import requests

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader
from .models import KnowledgeBase

GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
# تقدر تغيّر الاسم من البيئة؛ لاحظ تنسيق v1 الصحيح: يبدأ بـ models/
MODEL_NAME = (os.getenv("GEMINI_MODEL") or "models/gemini-1.5-flash").strip()

# Safety settings (نخليها أخف ما يمكن)
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def _read_latest_kb_text(max_chars: int = 60000) -> str:
    """يقرأ أحدث دليل/FAQ من قاعدة المعرفة (يدعم التخزين المحلي و Cloudinary)."""
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # أولوية: النص إن وُجد
    text = (getattr(kb, "content", "") or "").strip()
    if text:
        return text[:max_chars]

    f = getattr(kb, "file", None)
    if not f:
        return ""

    # جرّب القراءة مباشرة من التخزين
    data = None
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
    except Exception:
        data = None

    # لو فشلت (كلاودينري مثلاً) نحمّل من الرابط العام
    if data is None:
        url = getattr(f, "url", None)
        if not url:
            return ""
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.content

    # استخراج نص من PDF
    try:
        reader = PdfReader(BytesIO(data))
        parts = []
        total = 0
        for p in reader.pages:
            t = (p.extract_text() or "").strip()
            if t:
                parts.append(t)
                total += len(t)
                if total >= max_chars:
                    break
        return ("\n".join(parts))[:max_chars].strip()
    except Exception:
        return ""


def ask_gemini(user_prompt: str) -> str:
    """استدعاء Gemini v1 مباشرة عبر REST (بدون SDK)."""
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    kb_text = _read_latest_kb_text()

    system_rule = (
        "أنت UniBot 🎓، المساعد الذكي الرسمي للجامعة."
        " أجب بالعربية الفصحى، وبناءً فقط على محتوى الدليل المرفق."
        " إن لم تجد الإجابة في النص، قل: «عذرًا، المعلومة غير متوفرة في الدليل الحالي.»"
    )

    prompt_text = f"""{system_rule}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

    url = f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "safetySettings": SAFETY_SETTINGS,
    }

    try:
        r = requests.post(url, json=payload, timeout=60)
        # لو ردّ 404 هنا، بيكون واضح أنه اسم الموديل غلط، مو v1beta
        r.raise_for_status()
        data = r.json()
        text = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
        ).strip()

        if not text:
            return "عذرًا، المعلومة غير متوفرة في الدليل الحالي."
        return text
    except requests.HTTPError as e:
        try:
            detail = r.json()
        except Exception:
            detail = {}
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {e} | {detail}"
    except Exception as e:
        return f"⚠️ خطأ في الاتصال: {e}"
