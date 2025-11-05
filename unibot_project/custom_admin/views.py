from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from core.models import (
    Event,
    Category,
    FAQ,
    Favorite,
    Feedback,
    CustomUser,
    KnowledgeBase,
)

# ======== Forms ========
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "start_date", "end_date", "location", "description", "image"]

# ======== Dashboard ========
@staff_member_required
def dashboard(request):
    now = timezone.now()
    stats = {
        "users": CustomUser.objects.count(),
        "faqs": FAQ.objects.count(),
        "upcoming_events": Event.objects.filter(start_date__gte=now).count(),
    }
    recent_events = Event.objects.order_by("-updated_at")[:6]
    return render(
        request,
        "custom_admin/dashboard.html",
        {"stats": stats, "recent_events": recent_events, "now": now},
    )

# ======== Events ========
@staff_member_required
def events_list(request):
    qs = Event.objects.order_by("-start_date")
    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(location__icontains=q) | Q(slug__icontains=q))
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/events_list.html", {"events": items, "q": q or ""})

@staff_member_required
def event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/event_add.html", {"form": form})

# ======== Categories ========
@staff_member_required
def categories_list(request):
    q = request.GET.get("q", "")
    qs = Category.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    qs = qs.order_by("name")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/categories_list.html", {"items": items, "q": q})

# ======== FAQs ========
@staff_member_required
def faqs_list(request):
    q = request.GET.get("q", "")
    qs = FAQ.objects.select_related("category", "updated_by")
    if q:
        qs = qs.filter(Q(question__icontains=q) | Q(answer__icontains=q))
    qs = qs.order_by("-updated_at")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/faqs_list.html", {"items": items, "q": q})

# ======== Favorites ========
@staff_member_required
def favorites_list(request):
    qs = Favorite.objects.select_related("user", "faq").order_by("-created_at")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/favorites_list.html", {"items": items})

# ======== Feedback ========
@staff_member_required
def feedback_list(request):
    qs = Feedback.objects.select_related("faq", "user").order_by("-created_at")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/feedback_list.html", {"items": items})

# ======== Users ========
@staff_member_required
def users_list(request):
    q = request.GET.get("q", "")
    qs = CustomUser.objects.all()
    if q:
        qs = qs.filter(Q(email__icontains=q) | Q(name__icontains=q))
    qs = qs.order_by("-created_at")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/users_list.html", {"items": items, "q": q})

# ======== Knowledge Base ========
@staff_member_required
def knowledgebases_list(request):
    q = request.GET.get("q", "")
    qs = KnowledgeBase.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)
    qs = qs.order_by("-updated_at")
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "custom_admin/kb_list.html", {"items": items, "q": q})
