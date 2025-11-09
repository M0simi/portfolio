import os
from io import BytesIO
import requests  # <-- سنستخدم هذه المكتبة

import google.generativeai as genai

# --- (هذا الكود لإعدادات الأمان سليم) ---
try:
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    _HC  = HarmCategory
    _HBT = HarmBlockThreshold
    SAFETY_SETTINGS = [
        {"category": getattr(_HC,  "HARM_CATEGORY_HATE_SPEECH",       "HARM_CATEGORY_HATE_SPEECH"),      "threshold": getattr(_HBT, "BLOCK_NONE", "BLOCK_NONE")},
        {"category": getattr(_HC,  "HARM_CATEGORY_HARASSMENT",        "HARM_CATEGORY_HARASSMENT"),       "threshold": getattr(_HBT, "BLOCK_NONE", "BLOCK_NONE")},
        {"category": getattr(_HC,  "HARM_CATEGORY_SEXUAL_CONTENT",    "HARM_CATEGORY_SEXUAL_CONTENT"),   "threshold": getattr(_HBT, "BLOCK_NONE", "BLOCK_NONE")},
        {"category": getattr(_HC,  "HARM_CATEGORY_DANGEROUS_CONTENT", "HARM_CATEGORY_DANGEROUS_CONTENT"),"threshold": getattr(_HBT, "BLOCK_NONE", "BLOCK_NONE")},
    ]
except Exception:
    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUAL_CONTENT",    "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

from django.core.files.storage import default_storage
from PyPDF2 import PdfReader

from .models import KnowledgeBase

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME     = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

GEN_CFG = {"temperature": 0.2, "max_output_tokens": 2048}


def _read_latest_kb_text(max_chars: int = 60_000) -> str:
    """
    (الحل الجذري)
    يقرأ أحدث ملف PDF عن طريق تحميله من رابطه العام مباشرة (لتجاوز 401).
    """
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""

    # النص المباشر إن وُجد
    content_text = (getattr(kb, "content", "") or "").strip()
    if content_text:
        return content_text[:max_chars]

    # ملف مرفوع (PDF)
    f = getattr(kb, "file", None)
    if not f:
        return ""

    # --- 🚀 هذا هو التعديل الكامل (الخطة ب) ---
    
    file_url = f.url  # <-- نحصل على الرابط العام (Public URL)
    if not file_url:
        raise RuntimeError("الملف موجود في قاعدة البيانات ولكن ليس له رابط URL.")

    try:
        # نتظاهر بأننا متصفح (Browser) لتجنب الحظر
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # نقوم بتحميل الرابط العام
        response = requests.get(file_url, headers=headers)
        response.raise_for_status() # سيعطي خطأ إذا كان الرابط 404 أو 403
        
        data = response.content # هذا هو محتوى الملف (بايت)

    except requests.RequestException as e:
        # هذا سيمسك أي خطأ في تحميل الرابط
        raise RuntimeError(f"فشل تحميل الملف من الرابط العام: {e}")
    # --- نهاية التعديل ---

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
    """
    يولّد إجابة بالاعتماد على الدليل/الأسئلة المرفوعة.
    """
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."

    try:
        # الكود الآن سيستخدم الدالة المعدلة في الأعلى
        kb_text = _read_latest_kb_text()

        system_rule = (
            "أنت UniBot 🎓، المساعد الذكي الرسمي للجامعة. "
            "أجب بالعربية الفصحى، وبالاعتماد الحصري على النص التالي من الدليل. "
            "إن لم تجد الإجابة في النص، قل: "
            "«عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة.»"
        )

        prompt = f"""{system_rule}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

        last_err = None
        # (استخدام set() لإزالة التكرار إذا كان MODEL_NAME هو نفسه "gemini-1.5-flash")
        for name in set([MODEL_NAME, "gemini-1.5-flash"]): 
            try:
                model = genai.GenerativeModel(
                    model_name=name,
                    safety_settings=SAFETY_SETTINGS,
                    generation_config=GEN_CFG,
                )
                resp = model.generate_content(prompt)

                if not getattr(resp, "candidates", None):
                    return "عذرًا، تم حظر الرد لأسباب تتعلق بالأمان. حاول إعادة صياغة السؤال."

                text = (getattr(resp, "text", "") or "").strip()
                if not text:
                    return ("عذرًا، المعلومة التي تبحث عنها غير متوفرة في الدليل الحالي. "
                            "للحصول على تفاصيل أدق، أنصحك بمراجعة القسم المختص في الجامعة.")
                
                for kw in ("حسب الملف", "وفقًا للمستند", "PDF", "الملف"):
                    text = text.replace(kw, "")
                return text.strip()

            except Exception as e:
                last_err = e
                continue

        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {last_err}"

    except Exception as e:
        # الآن إذا فشل، سيظهر لنا الخطأ من 'requests'
        return f"⚠️ خطأ في الإعداد أو قراءة الملف: {e}"
