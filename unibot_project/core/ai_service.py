import os
from io import BytesIO
import requests

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase


# =========================
# إعدادات عامة
# =========================
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
# يمكنك تغييره من متغير البيئة، لكن تأكد أن يبدأ بـ models/
GEMINI_MODEL = (os.getenv("GEMINI_MODEL") or "models/gemini-1.5-flash").strip()
if not GEMINI_MODEL.startswith("models/"):
    GEMINI_MODEL = "models/" + GEMINI_MODEL

REST_HOST = "https://generativelanguage.googleapis.com/v1"


# =========================
# قراءة أحدث ملف معرفة (نص/ PDF)
# =========================
def _kb_excerpt(max_chars: int = 60_000) -> str:
    """
    يرجع مقتطف نصي من أحدث عنصر في KnowledgeBase:
    - لو فيه content نصي: نستخدمه.
    - غير كذا: نحاول نقرأ PDF من التخزين (محلي) وإن فشل نستخدم الرابط العام (Cloudinary).
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # 1) محتوى نصّي مباشر
    content = (getattr(kb, "content", "") or "").strip()
    if content:
        return content[:max_chars]

    # 2) ملف PDF
    f = getattr(kb, "file", None)
    if not f:
        return ""

    data = None

    # نحاول القراءة من التخزين المعرّف (محلي/سحابي يدعم .open)
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
    except Exception:
        data = None

    # لو فشلنا، نحاول عبر الرابط العام (Cloudinary raw)
    if data is None:
        file_url = getattr(f, "url", None)
        if not file_url:
            return ""
        r = requests.get(file_url, timeout=30)
        r.raise_for_status()
        data = r.content

    # استخراج النص من PDF
    try:
        reader = PdfReader(BytesIO(data))
        parts, total = [], 0
        for p in reader.pages:
            t = p.extract_text() or ""
            if t:
                parts.append(t)
                total += len(t)
                if total >= max_chars:
                    break
        return ("\n".join(parts))[:max_chars].strip()
    except Exception:
        # لو فشل الاستخراج نرجع فاضي (والـ ask_gemini يتعامل)
        return ""


# =========================
# استدعاء REST v1 مباشرة
# =========================
def _rest_generate(prompt: str, api_key: str, model: str) -> str:
    """
    اتصال مباشر بنقطة: POST /v1/{model}:generateContent
    يُرجع النص أو رسالة تشخيصية واضحة عند 404 مع أسماء النماذج المتاحة لمفتاحك.
    """
    url = f"{REST_HOST}/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        # إطفاء كل الفلاتر (جامعات كثير فيها كلمات قد تُفسّر على أنها حساسة)
        "safetySettings": [
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    }

    r = requests.post(url, json=payload, timeout=60)

    # تشخيص خاص لو موديل مش متاح/خطأ 404
    if r.status_code == 404:
        try:
            detail = r.json()
        except Exception:
            detail = {"raw": r.text}

        # نحاول نجيب قائمة النماذج المتاحة فعلياً لهذا المفتاح
        try:
            list_url = f"{REST_HOST}/models?key={api_key}"
            mm = requests.get(list_url, timeout=30)
            names = []
            if mm.ok:
                j = mm.json()
                names = [m.get("name", "") for m in j.get("models", [])]
        except Exception:
            names = []

        hint_lines = ["REST v1 → 404 للموديل:", f"- {model}", "نماذج API المتاحة لمفتاحك:"]
        if names:
            hint_lines += [f"- {n}" for n in names[:20]]
        else:
            hint_lines.append("- (تعذر جلب القائمة أو لا توجد نماذج متاحة)")
        return "\n".join(hint_lines)

    r.raise_for_status()
    data = r.json()
    text = (
        (data.get("candidates") or [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    ).strip()

    if not text:
        text = "عذرًا، المعلومة غير متوفرة في الدليل الحالي."
    return text


# =========================
# الواجهة المستعملة من views.py
# =========================
def ask_gemini(user_prompt: str) -> str:
    """
    يُبنى البرومبت بالعربية ويُمرَّر لنقطة REST v1. لا يعتمد على google-generativeai SDK.
    """
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    guide = _kb_excerpt() or "لا يتوفر محتوى معرفة حالياً."

    system_rule = (
        "أنت UniBot 🎓 — مساعد جامعي باللغة العربية الفصحى."
        " أجب فقط بناءً على النص التالي المستخرج من دليل الجامعة."
        " إن لم تجد الإجابة صرّح بذلك بوضوح."
    )

    prompt = f"""{system_rule}

--- مقتطف من الدليل ---
{guide}

--- سؤال المستخدم ---
{user_prompt}
"""

    try:
        return _rest_generate(prompt, GEMINI_API_KEY, GEMINI_MODEL)
    except requests.HTTPError as e:
        # نحاول إرجاع سبب HTTP
        try:
            j = e.response.json()
        except Exception:
            j = {"raw": e.response.text if e.response is not None else str(e)}
        return f"REST v1 HTTP error: {j}"
    except Exception as e:
        return f"REST v1 error: {e}"
