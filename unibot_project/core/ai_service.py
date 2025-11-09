# ai_service.py
import os
from io import BytesIO

import requests
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase

# =======================
# إعداد مفتاح ونوع الموديل
# =======================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.0-pro").strip()   

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

def _read_latest_kb_text(max_chars: int = 60_000) -> str:
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    text = (getattr(kb, "content", "") or "").strip()
    if text:
        return text[:max_chars]

    f = getattr(kb, "file", None)
    if not f:
        return ""

    data = None
    try:
        with default_storage.open(f.name, "rb") as fh:
            data = fh.read()
    except Exception:
        data = None

    if data is None:
        file_url = getattr(f, "url", None)
        if not file_url:
            return ""
        try:
            r = requests.get(file_url, timeout=30)
            r.raise_for_status()
            data = r.content
        except Exception:
            return ""

    try:
        reader = PdfReader(BytesIO(data))
        parts, total = [], 0
        for p in reader.pages:
            t = (p.extract_text() or "")
            if t:
                parts.append(t)
                total += len(t)
                if total >= max_chars:
                    break
        return ("\n".join(parts))[:max_chars].strip()
    except Exception:
        return ""

def ask_gemini(user_prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    kb_text = _read_latest_kb_text()

    system_rule = (
        "أنت UniBot 🎓، المساعد الذكي الرسمي لجامعتنا. "
        "استخدم العربية الفصحى. لا تُنشئ معلومات غير موجودة بالدليل. "
        "إن لم تجد الإجابة في النص، قل: «عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي.»"
    )

    prompt = f"""{system_rule}
--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}
--- سؤال المستخدم ---
{user_prompt}
"""

    for name in [MODEL_NAME, "gemini-1.5-flash-latest"]:
        try:
            model = genai.GenerativeModel(name, safety_settings=SAFETY_SETTINGS)
            resp = model.generate_content(prompt)

            if not getattr(resp, "candidates", None):
                return "عذرًا، تم حظر الرد لأسباب تتعلق بالأمان. حاول إعادة صياغة السؤال."

            text = (getattr(resp, "text", "") or "").strip()
            if not text:
                text = "عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي."
            return text
        except Exception as e:
            last_err = e
            continue

    return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err}"
