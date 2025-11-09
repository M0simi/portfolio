# custom_admin/forms.py
from django import forms
from django.contrib.auth import get_user_model
from core.models import Event, FAQ, Category, KnowledgeBase

User = get_user_model()


# =========================
# Events
# =========================
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "description", "start_date", "end_date", "location", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "عنوان الحدث"}),
            "slug": forms.TextInput(attrs={"placeholder": "slug (يُملأ تلقائيًا إن تركته فارغًا)"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "وصف مختصر"}),
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "location": forms.TextInput(attrs={"placeholder": "الموقع"}),
        }


# =========================
# FAQs
# =========================
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "category", "updated_by"]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 3, "placeholder": "نص السؤال"}),
            "answer": forms.Textarea(attrs={"rows": 6, "placeholder": "الإجابة"}),
            "category": forms.Select(),
            "updated_by": forms.Select(),
        }


# =========================
# Categories
# =========================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "اسم الفئة"}),
        }


# =========================
# Knowledge Base
# =========================
class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "عنوان الملف/المصدر"}),
            # الملف يُدار تلقائياً عبر حقل FileField
        }


# =========================
# Users (اختياري لإدارة مبسطة)
# =========================
class UserRoleForm(forms.ModelForm):
    """
    إدارة مبسطة للمستخدم: تغيير الدور و is_staff فقط (بدون كلمات مرور).
    """
    class Meta:
        model = User
        fields = ["name", "email", "role", "is_staff", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "الاسم"}),
            "email": forms.EmailInput(attrs={"placeholder": "البريد"}),
            "role": forms.Select(),
        }
        help_texts = {
            "is_staff": "يمنح صلاحية الدخول للوحة التحكم المخصصة.",
        }
