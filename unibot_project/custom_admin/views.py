from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from core.models import (
    Event,
    Category,
    FAQ,
    Favorite,
    Feedback,
    CustomUser,
    KnowledgeBase,
)

# -------- Forms --------
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "start_date", "end_date", "location", "description", "image"]

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "category"]

class KnowledgeBaseForm(ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ["title", "file"]


# -------- Dashboard --------
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


# -------- Events --------
@staff_member_required
def events_list(request):
    qs = Event.objects.order_by("-start_date")
    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(location__icontains=q) | Q(slug__icontains=q))
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/events_list.html", {"events": items, "q": q or ""})

@staff_member_required
def event_add(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event created.")
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Add Event", "form": form})

@staff_member_required
def event_edit(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event updated.")
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Edit Event", "form": form})

@staff_member_required
def event_delete(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Event deleted.")
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})


# -------- Categories --------
@staff_member_required
def categories_list(request):
    q = request.GET.get("q", "")
    qs = Category.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    qs = qs.order_by("name")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/categories_list.html", {"items": items, "q": q})

@staff_member_required
def category_add(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created.")
        return redirect("custom_admin:categories_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Add Category", "form": form})

@staff_member_required
def category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated.")
        return redirect("custom_admin:categories_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Edit Category", "form": form})

@staff_member_required
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Category deleted.")
        return redirect("custom_admin:categories_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})


# -------- FAQs --------
@staff_member_required
def faqs_list(request):
    q = request.GET.get("q", "")
    qs = FAQ.objects.select_related("category", "updated_by")
    if q:
        qs = qs.filter(Q(question__icontains=q) | Q(answer__icontains=q))
    qs = qs.order_by("-updated_at")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/faqs_list.html", {"items": items, "q": q})

@staff_member_required
def faq_add(request):
    form = FAQForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "FAQ created.")
        return redirect("custom_admin:faqs_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Add FAQ", "form": form})

@staff_member_required
def faq_edit(request, pk):
    obj = get_object_or_404(FAQ, pk=pk)
    form = FAQForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "FAQ updated.")
        return redirect("custom_admin:faqs_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Edit FAQ", "form": form})

@staff_member_required
def faq_delete(request, pk):
    obj = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "FAQ deleted.")
        return redirect("custom_admin:faqs_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})


# -------- Favorites --------
@staff_member_required
def favorites_list(request):
    qs = Favorite.objects.select_related("user", "faq").order_by("-created_at")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/favorites_list.html", {"items": items})

@staff_member_required
def favorite_delete(request, pk):
    obj = get_object_or_404(Favorite, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Favorite deleted.")
        return redirect("custom_admin:favorites_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})


# -------- Feedback --------
@staff_member_required
def feedback_list(request):
    qs = Feedback.objects.select_related("faq", "user").order_by("-created_at")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/feedback_list.html", {"items": items})

@staff_member_required
def feedback_delete(request, pk):
    obj = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Feedback deleted.")
        return redirect("custom_admin:feedback_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})


# -------- Users (read-only list) --------
@staff_member_required
def users_list(request):
    q = request.GET.get("q", "")
    qs = CustomUser.objects.all()
    if q:
        qs = qs.filter(Q(email__icontains=q) | Q(name__icontains=q))
    qs = qs.order_by("-created_at")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/users_list.html", {"items": items, "q": q})


# -------- Knowledge Base --------
@staff_member_required
def knowledgebases_list(request):
    q = request.GET.get("q", "")
    qs = KnowledgeBase.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)
    qs = qs.order_by("-updated_at")
    paginator = Paginator(qs, 20)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "custom_admin/kb_list.html", {"items": items, "q": q})

@staff_member_required
def kb_add(request):
    form = KnowledgeBaseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "File added.")
        return redirect("custom_admin:knowledgebases_list")
    return render(request, "custom_admin/generic_form.html", {"title": "Add Knowledge Base", "form": form})

@staff_member_required
def kb_delete(request, pk):
    obj = get_object_or_404(KnowledgeBase, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "File deleted.")
        return redirect("custom_admin:knowledgebases_list")
    return render(request, "custom_admin/generic_confirm_delete.html", {"title": "Confirm delete", "obj": obj})
