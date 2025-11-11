from django import forms
from core.models import Event, Category, FAQ, Favorite, Feedback, CustomUser, KnowledgeBase

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "description", "start_date", "end_date", "location", "image"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["category", "question", "answer"]

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["user", "faq"]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["faq", "user", "helpful", "comment"]

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "role", "is_active", "is_staff", "is_superuser"]

class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]
