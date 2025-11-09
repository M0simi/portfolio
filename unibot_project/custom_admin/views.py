from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Event, FAQ, CustomUser
from .forms import EventForm


@staff_member_required
def dashboard(request):
    """لوحة التحكم الرئيسية: إحصائيات + آخر العناصر"""
    stats = {
        "events_count": Event.objects.count(),
        "faqs_count": FAQ.objects.count(),
        "users_count": CustomUser.objects.count(),
    }
    latest_events = Event.objects.order_by("-start_date")[:5]
    latest_faqs = FAQ.objects.order_by("-id")[:5]
    return render(request, "custom_admin/dashboard.html", {
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
        "title": "لوحة التحكّم | UniBot",
    })


# =========================
# Events CRUD
# =========================
@staff_member_required
def events_list(request):
    """قائمة الأحداث مع بحث وترقيم"""
    q = request.GET.get("q", "").strip()
    qs = Event.objects.all().order_by("-start_date")
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(location__icontains=q) |
            Q(description__icontains=q)
        )
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "custom_admin/events_list.html", {
        "title": "إدارة الأحداث",
        "q": q,
        "count": qs.count(),
        "page_obj": page_obj,
    })


@staff_member_required
def event_add(request):
    """إضافة حدث جديد"""
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"تم إنشاء الحدث «{obj.title}» بنجاح.")
            return redirect("custom_admin:events_list")
        messages.error(request, "تعذر حفظ النموذج. فضلاً تحقق من الحقول.")
    else:
        form = EventForm()

    return render(request, "custom_admin/generic_form.html", {
        "title": "إضافة حدث",
        "form": form,
        "submit_label": "حفظ",
        "back_url": "custom_admin:events_list",
        "enctype_multipart": True,  # ضروري لرفع الصورة
    })


@staff_member_required
def event_edit(request, pk):
    """تعديل حدث"""
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"تم تحديث الحدث «{obj.title}».")
            return redirect("custom_admin:events_list")
        messages.error(request, "تعذر حفظ التعديلات. فضلاً تحقق من الحقول.")
    else:
        form = EventForm(instance=obj)

    return render(request, "custom_admin/generic_form.html", {
        "title": f"تعديل: {obj.title}",
        "form": form,
        "submit_label": "تحديث",
        "back_url": "custom_admin:events_list",
        "enctype_multipart": True,
    })


@staff_member_required
def event_delete(request, pk):
    """حذف حدث مع تأكيد"""
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        title = obj.title
        obj.delete()
        messages.success(request, f"تم حذف الحدث «{title}».")
        return redirect("custom_admin:events_list")

    return render(request, "custom_admin/generic_confirm_delete.html", {
        "title": f"حذف: {obj.title}",
        "object": obj,
        "back_url": "custom_admin:events_list",
    })
