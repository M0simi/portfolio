import os
import requests
import PyPDF2
from core.models import KnowledgeBase  

# قراءة مفتاح Gemini من متغيرات البيئة
API_KEY = os.getenv("GEMINI_API_KEY")

def load_latest_pdf_text():
    """
    تحميل نص آخر ملف PDF تم رفعه في قاعدة المعرفة.
    """
    kb = KnowledgeBase.objects.order_by('-id').first()
    if not kb:
        return "❌ لا يوجد أي ملف مرفوع في قاعدة المعرفة."

    pdf_path = kb.file.path
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
        return text.strip()
    except Exception as e:
        return f"⚠️ خطأ أثناء قراءة الملف: {e}"


def ask_gemini(prompt: str) -> str:
    """
    يرسل السؤال إلى نموذج Gemini مع تضمين محتوى ملف PDF من قاعدة المعرفة.
    """
    if not API_KEY:
        return "❌ لم يتم العثور على مفتاح GEMINI_API_KEY في الإعدادات."

    # قراءة نص PDF من قاعدة البيانات
    pdf_text = load_latest_pdf_text()
    if pdf_text.startswith("❌") or pdf_text.startswith("⚠️"):
        return pdf_text  # خطأ في تحميل الملف

    # إعداد الطلب الكامل
    full_prompt = f"""
السؤال: {prompt}

---
المحتوى المستند إليه من الملف (للمساعدة في الإجابة):
{pdf_text[:5000]}
---
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={API_KEY}"
    )

    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "❌ لم يتم العثور على رد.")
        )
    except Exception as e:
        return f"⚠️ خطأ أثناء الاتصال بـ Gemini API: {str(e)}"

