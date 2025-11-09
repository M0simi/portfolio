from django import forms
from core.models import (
    Event,
    FAQ,
    Category,
    KnowledgeBase,
    Feedback,
    Favorite,
    CustomUser,
)

# === Widgets وتهيئة ===
_DT_WIDGET = forms.DateTimeInput(attrs={"type": "datetime-local"})
_TEXTAREA = forms.Textarea(attrs={"rows": 4})
_DATETIME_INPUT_FORMATS = [
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M",
]


# =========================
# الفعاليات
# =========================
class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=_DT_WIDGET, input_formats=_DATETIME_INPUT_FORMATS
    )
    end_date = forms.DateTimeField(
        required=False, widget=_DT_WIDGET, input_formats=_DATETIME_INPUT_FORMATS
    )
    description = forms.CharField(widget=_TEXTAREA, required=False)

    class Meta:
        model = Event
        fields = ["title", "start_date", "end_date", "location", "description", "image"]

    def clean(self):
        cleaned = super().clean()
        sd = cleaned.get("start_date")
        ed = cleaned.get("end_date")
        if sd and ed and ed < sd:
            self.add_error("end_date", "تاريخ النهاية يجب أن يكون بعد البداية.")
        return cleaned


# =========================
# الأسئلة الشائعة
# =========================
class FAQForm(forms.ModelForm):
    question = forms.CharField(widget=_TEXTAREA)
    answer = forms.CharField(widget=_TEXTAREA)

    class Meta:
        model = FAQ
        fields = ["question", "answer", "category", "updated_by"]


# =========================
# الفئات
# =========================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


# =========================
# قاعدة المعرفة
# =========================
class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]

    def clean_file(self):
        # الملف اختياري
        return self.cleaned_data.get("file")


# =========================
# التعليقات (حذف/إدارة بسيطة)
# =========================
class FeedbackDeleteForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = []


# =========================
# المفضلات (حذف)
# =========================
class FavoriteDeleteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []


# =========================
# المستخدمون
# =========================
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False, help_text="البريد لا يمكن تعديله.")

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "name",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


# نموذج مبسّط لتغيير الدور فقط (مطلوب في views.py)
class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["role"]
