from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

from core.models import (
    Event,
    FAQ,
    Category,
    Feedback,
    Favorite,
    KnowledgeBase,
    CustomUser,
)
from .forms import (
    EventForm,
    FAQForm,
    CategoryForm,
    KnowledgeBaseForm,
    UserRoleForm,
)

User = get_user_model()


# =========================
# Dashboard
# =========================
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
    return render(
        request,
        "custom_admin/dashboard.html",
        {
            "stats": stats,
            "latest_events": latest_events,
            "latest_faqs": latest_faqs,
            "title": "لوحة التحكّم | UniBot",
        },
    )


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
            Q(title__icontains=q)
            | Q(location__icontains=q)
            | Q(description__icontains=q)
        )
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/events_list.html",
        {
            "title": "إدارة الأحداث",
            "q": q,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


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

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "إضافة حدث",
            "form": form,
            "submit_label": "حفظ",
            "back_url": "custom_admin:events_list",
            "enctype_multipart": True,  # لرفع الصورة
        },
    )


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

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": f"تعديل: {obj.title}",
            "form": form,
            "submit_label": "تحديث",
            "back_url": "custom_admin:events_list",
            "enctype_multipart": True,
        },
    )


@staff_member_required
def event_delete(request, pk):
    """حذف حدث مع تأكيد"""
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        title = obj.title
        obj.delete()
        messages.success(request, f"تم حذف الحدث «{title}».")
        return redirect("custom_admin:events_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": f"حذف: {obj.title}",
            "object": obj,
            "back_url": "custom_admin:events_list",
        },
    )


# =========================
# FAQs CRUD
# =========================
@staff_member_required
def faqs_list(request):
    """قائمة الأسئلة الشائعة مع بحث وترتيب"""
    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    qs = FAQ.objects.select_related("category", "updated_by").order_by("-updated_at")
    if q:
        qs = qs.filter(Q(question__icontains=q) | Q(answer__icontains=q))
    if category_id:
        qs = qs.filter(category_id=category_id)

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    categories = Category.objects.order_by("name")

    return render(
        request,
        "custom_admin/faqs_list.html",
        {
            "title": "إدارة الأسئلة الشائعة",
            "q": q,
            "category_id": category_id,
            "categories": categories,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def faq_add(request):
    """إضافة سؤال شائع"""
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "تمت إضافة السؤال الشائع بنجاح.")
            return redirect("custom_admin:faqs_list")
        messages.error(request, "تعذر حفظ النموذج. فضلاً تحقق من الحقول.")
    else:
        form = FAQForm()

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "إضافة سؤال شائع",
            "form": form,
            "submit_label": "حفظ",
            "back_url": "custom_admin:faqs_list",
        },
    )


@staff_member_required
def faq_edit(request, pk):
    """تعديل سؤال شائع"""
    obj = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        form = FAQForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث السؤال الشائع.")
            return redirect("custom_admin:faqs_list")
        messages.error(request, "تعذر حفظ التعديلات. فضلاً تحقق من الحقول.")
    else:
        form = FAQForm(instance=obj)

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "تعديل سؤال شائع",
            "form": form,
            "submit_label": "تحديث",
            "back_url": "custom_admin:faqs_list",
        },
    )


@staff_member_required
def faq_delete(request, pk):
    """حذف سؤال شائع"""
    obj = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "تم حذف السؤال الشائع.")
        return redirect("custom_admin:faqs_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": "حذف سؤال شائع",
            "object": obj,
            "back_url": "custom_admin:faqs_list",
        },
    )


# =========================
# Categories CRUD
# =========================
@staff_member_required
def categories_list(request):
    q = request.GET.get("q", "").strip()
    qs = Category.objects.order_by("name")
    if q:
        qs = qs.filter(name__icontains=q)
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/categories_list.html",
        {
            "title": "إدارة الفئات",
            "q": q,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة الفئة.")
            return redirect("custom_admin:categories_list")
        messages.error(request, "تعذر حفظ النموذج.")
    else:
        form = CategoryForm()

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "إضافة فئة",
            "form": form,
            "submit_label": "حفظ",
            "back_url": "custom_admin:categories_list",
        },
    )


@staff_member_required
def category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الفئة.")
            return redirect("custom_admin:categories_list")
        messages.error(request, "تعذر حفظ التعديلات.")
    else:
        form = CategoryForm(instance=obj)

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "تعديل فئة",
            "form": form,
            "submit_label": "تحديث",
            "back_url": "custom_admin:categories_list",
        },
    )


@staff_member_required
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "تم حذف الفئة.")
        return redirect("custom_admin:categories_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": "حذف فئة",
            "object": obj,
            "back_url": "custom_admin:categories_list",
        },
    )


# =========================
# Knowledge Base CRUD
# =========================
@staff_member_required
def kb_list(request):
    q = request.GET.get("q", "").strip()
    qs = KnowledgeBase.objects.order_by("-updated_at")
    if q:
        qs = qs.filter(Q(title__icontains=q))
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/kb_list.html",
        {
            "title": "إدارة قاعدة المعرفة",
            "q": q,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def kb_add(request):
    if request.method == "POST":
        form = KnowledgeBaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة المصدر بنجاح.")
            return redirect("custom_admin:kb_list")
        messages.error(request, "تعذر حفظ النموذج. تحقّق من الحقول.")
    else:
        form = KnowledgeBaseForm()

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "إضافة مصدر",
            "form": form,
            "submit_label": "حفظ",
            "back_url": "custom_admin:kb_list",
            "enctype_multipart": True,
        },
    )


@staff_member_required
def kb_edit(request, pk):
    obj = get_object_or_404(KnowledgeBase, pk=pk)
    if request.method == "POST":
        form = KnowledgeBaseForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث المصدر.")
            return redirect("custom_admin:kb_list")
        messages.error(request, "تعذر حفظ التعديلات.")
    else:
        form = KnowledgeBaseForm(instance=obj)

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": "تعديل مصدر",
            "form": form,
            "submit_label": "تحديث",
            "back_url": "custom_admin:kb_list",
            "enctype_multipart": True,
        },
    )


@staff_member_required
def kb_delete(request, pk):
    obj = get_object_or_404(KnowledgeBase, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "تم حذف المصدر.")
        return redirect("custom_admin:kb_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": "حذف مصدر",
            "object": obj,
            "back_url": "custom_admin:kb_list",
        },
    )


# =========================
# Feedback (عرض/حذف)
# =========================
@staff_member_required
def feedback_list(request):
    helpful = request.GET.get("helpful", "").strip()
    q = request.GET.get("q", "").strip()

    qs = (
        Feedback.objects.select_related("faq", "user")
        .order_by("-created_at")
    )
    if helpful in ("true", "false"):
        qs = qs.filter(helpful=(helpful == "true"))
    if q:
        qs = qs.filter(Q(faq__question__icontains=q) | Q(comment__icontains=q))

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/feedback_list.html",
        {
            "title": "التعليقات (Feedback)",
            "q": q,
            "helpful": helpful,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def feedback_delete(request, pk):
    obj = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "تم حذف التعليق.")
        return redirect("custom_admin:feedback_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": "حذف تعليق",
            "object": obj,
            "back_url": "custom_admin:feedback_list",
        },
    )


# =========================
# Favorites (عرض/حذف)
# =========================
@staff_member_required
def favorites_list(request):
    q = request.GET.get("q", "").strip()
    qs = Favorite.objects.select_related("user", "faq").order_by("-created_at")
    if q:
        qs = qs.filter(Q(user__email__icontains=q) | Q(faq__question__icontains=q))

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/favorites_list.html",
        {
            "title": "المفضلات",
            "q": q,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def favorites_delete(request, pk):
    obj = get_object_or_404(Favorite, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "تم حذف السجل من المفضلة.")
        return redirect("custom_admin:favorites_list")

    return render(
        request,
        "custom_admin/generic_confirm_delete.html",
        {
            "title": "حذف من المفضلة",
            "object": obj,
            "back_url": "custom_admin:favorites_list",
        },
    )


# =========================
# Users (إدارة مبسطة)
# =========================
@staff_member_required
def users_list(request):
    q = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    staff = request.GET.get("staff", "").strip()

    qs = User.objects.all().order_by("-created_at")
    if q:
        qs = qs.filter(Q(email__icontains=q) | Q(name__icontains=q))
    if role:
        qs = qs.filter(role=role)
    if staff in ("true", "false"):
        qs = qs.filter(is_staff=(staff == "true"))

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "custom_admin/users_list.html",
        {
            "title": "إدارة المستخدمين",
            "q": q,
            "role": role,
            "staff": staff,
            "count": qs.count(),
            "page_obj": page_obj,
        },
    )


@staff_member_required
def user_edit(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserRoleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث بيانات المستخدم.")
            return redirect("custom_admin:users_list")
        messages.error(request, "تعذر حفظ التعديلات.")
    else:
        form = UserRoleForm(instance=obj)

    return render(
        request,
        "custom_admin/generic_form.html",
        {
            "title": f"تعديل مستخدم: {obj.email}",
            "form": form,
            "submit_label": "تحديث",
            "back_url": "custom_admin:users_list",
        },
    )
