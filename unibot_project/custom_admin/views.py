from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.db.models import Q, Count
from django.utils import timezone

from core.models import Event, FAQ, CustomUser

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "start_date", "end_date", "location", "description", "image"]

@staff_member_required
def dashboard(request):
    now = timezone.now()
    stats = {
        "users": CustomUser.objects.count(),
        "faqs": FAQ.objects.count(),
        "upcoming_events": Event.objects.filter(start_date__gte=now).count(),
    }
    recent_events = Event.objects.order_by("-updated_at")[:6]
    return render(request, "custom_admin/dashboard.html", {
        "stats": stats,
        "recent_events": recent_events,
        "now": now,
    })

@staff_member_required
def events_list(request):
    qs = Event.objects.order_by("-start_date")
    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(location__icontains=q) | Q(slug__icontains=q))
    return render(request, "custom_admin/events_list.html", {"events": qs, "q": q or ""})

@staff_member_required
def event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/event_add.html", {"form": form})
