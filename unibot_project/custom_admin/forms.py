from django import forms
from core.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "description", "start_date", "end_date", "location", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "عنوان الحدث"}),
            "slug": forms.TextInput(attrs={"class": "input", "placeholder": "slug (يُملأ تلقائيًا إن تركته فارغًا)"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "وصف مختصر"}),
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "location": forms.TextInput(attrs={"placeholder": "الموقع"}),
        }
