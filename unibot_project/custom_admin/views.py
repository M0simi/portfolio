from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.forms import ModelForm
from core.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "start_date", "end_date", "location", "description", "image"]

@staff_member_required
def dashboard(request):
    return render(request, "custom_admin/dashboard.html")

@staff_member_required
def events_list(request):
    events = Event.objects.order_by("-start_date")
    return render(request, "custom_admin/events_list.html", {"events": events})

@staff_member_required
def event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/event_add.html", {"form": form})
