# custom_admin/forms.py
from django import forms
from core.models import (
    Event, Category, FAQ, Favorite, Feedback, CustomUser, KnowledgeBase
)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "start_date", "end_date", "location", "description", "image"]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "category"]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 3}),
            "answer": forms.Textarea(attrs={"rows": 6}),
        }

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["user", "faq"]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["faq", "user", "helpful", "comment"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 4})}

class UserForm(forms.ModelForm):
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "name", "role", "is_active", "is_staff", "is_superuser"]

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user

class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]
