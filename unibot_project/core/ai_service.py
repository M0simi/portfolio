# core/ai_service.py
import os
from io import BytesIO
from PyPDF2 import PdfReader
import google.generativeai as genai
from core.models import KnowledgeBase

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def _read_latest_kb_bytes():
    kb = KnowledgeBase.objects.order_by('-id').first()
    if not kb:
        return None, "⚠️ لا يوجد ملف/محتوى في قاعدة المعرفة."

    
    content = (getattr(kb, 'content', '') or '').strip()
    if content:
        return content.encode('utf-8'), None

    f = getattr(kb, 'file', None)
    if not f:
        return None, "⚠️ لا يوجد ملف مرفوع في قاعدة المعرفة."

    try:
        with f.storage.open(f.name, 'rb') as fh:
            data = fh.read()
        return data, None
    except Exception as e:
        return None, f"⚠️ تعذّر فتح الملف من التخزين: {e}"

def _extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
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

def ask_gemini(user_prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "❌ لم يتم ضبط متغير البيئة GEMINI_API_KEY."

    kb_bytes, err = _read_latest_kb_bytes()
    if err:
        return err

   
    try:
        # محاولة اعتباره نص مباشرة
        pdf_text = kb_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # إذن هو PDF
        pdf_text = _extract_text_from_pdf_bytes(kb_bytes)

    if not pdf_text:
        return "⚠️ تعذّر استخراج نصوص من ملف قاعدة المعرفة."

    system_prompt = (
        "أنت UniBot 🎓 — مساعد جامعي ذكي ناطق بالعربية الفصحى. "
        "أجب فقط بناءً على النص التالي. "
        "إن لم تجد إجابة في النص، قل: عذرًا، سؤالك غير موجود في الملف الحالي."
    )
    full_prompt = f"{system_prompt}\n\n--- محتوى الدليل ---\n{pdf_text[:6000]}\n\n--- سؤال المستخدم ---\n{user_prompt}"

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(full_prompt)
        answer = (resp.text or "").strip()
        return answer or "عذرًا، سؤالك غير موجود في الملف الحالي."
    except Exception as e:
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini: {e}"
