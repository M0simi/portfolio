# core/ai_service.py
import os
from io import BytesIO
import google.generativeai as genai
from django.core.files.storage import default_storage
from PyPDF2 import PdfReader
from .models import KnowledgeBase

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest").strip()
MAX_CHARS = 60000


SAFETY_OFF = [
    {"category": "HARM_CATEGORY_HATE_SPEECH",     "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT",      "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUAL_CONTENT",  "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"},
]

def _load_kb_text():
    kb = KnowledgeBase.objects.order_by("-id").first()
    if not kb:
        return ""
    txt = (getattr(kb, "content", "") or "").strip()
    if txt:
        return txt[:MAX_CHARS]
    f = getattr(kb, "file", None)
    if not f:
        return ""
    try:
        with default_storage.open(f.name, "rb") as fp:
            data = fp.read()
    except Exception as e:
        return f"[KB-READ-ERROR] {e}"
    try:
        reader = PdfReader(BytesIO(data))
        parts = []
        acc = 0
        for p in reader.pages:
            t = (p.extract_text() or "")
            if t:
                parts.append(t)
                acc += len(t)
                if acc >= MAX_CHARS:
                    break
        return ("\n".join(parts)).strip()
    except Exception as e:
        return f"[KB-PARSE-ERROR] {e}"

def _clean(ans: str) -> str:
    if not ans:
        return ""
    for bad in ["حسب الملف", "وفقًا للمستند", "PDF", "الملف:"]:
        ans = ans.replace(bad, "")
    return ans.strip()

def ask_gemini(user_prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "❌ مفقود متغير البيئة GEMINI_API_KEY."
    genai.configure(api_key=GEMINI_API_KEY)

    kb_text = _load_kb_text()
    kb_note = ""
    if kb_text.startswith("[KB-READ-ERROR]") or kb_text.startswith("[KB-PARSE-ERROR]"):
        kb_note = kb_text
        kb_text = ""

    system_msg = (
        "أنت UniBot 🎓 — مساعد جامعي عربي فصيح. "
        "أجب إجابة معلوماتية ومحايدة مقتصرة على لوائح الجامعة فقط. "
        "إذا لم تجد الإجابة في النص المرفق، قل: «عذرًا، سؤالك غير موجود في الملف الحالي.» "
        "تجنب أي محتوى حساس أو خارج سياق اللوائح."
    )

    prompt = f"""{system_msg}

--- مقتطف من الدليل/الأسئلة ---
{kb_text if kb_text else "لا يتوفر محتوى معرفة حالياً."}

--- سؤال المستخدم ---
{user_prompt}
"""

    if kb_note:
        prompt += f"\n[ملاحظة تقنية]: {kb_note}\n"

   
    model = genai.GenerativeModel(
        MODEL,
        safety_settings=SAFETY_OFF,
        generation_config={"temperature": 0.2, "max_output_tokens": 2048},
    )

    try:
        resp = model.generate_content(prompt)
        # لو انحظر الرد (SAFETY) أو انتهى بلا نص، نجرب إعادة الصياغة
        text = getattr(resp, "text", "") or ""
        if not text:
            # ريتراي بصياغة أكثر “آمنة”
            retry = model.generate_content(
                f"أعد صياغة إجابة قصيرة ومعلوماتية للسؤال التالي بدون أي محتوى حساس:"
                f"\n\nالنص المسموح الاعتماد عليه:\n{kb_text[:4000]}\n\nالسؤال:\n{user_prompt}"
            )
            text = getattr(retry, "text", "") or ""

        text = _clean(text)
        if not text:
            text = "عذرًا، سؤالك غير موجود في الملف الحالي."
        return text

    except Exception as e:
        # نرجّع السبب نصًا عشان تشوفه في الواجهة
        return f"⚠️ حدث خطأ في خدمة الذكاء: {e}"
