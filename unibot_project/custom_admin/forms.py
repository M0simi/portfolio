from django import forms
from core.models import Category, FAQ, Favorite, Feedback, KnowledgeBase, Event

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "category"]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "start_date", "end_date", "image"]

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["user", "faq"]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["faq", "user", "helpful", "comment"]

class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]
