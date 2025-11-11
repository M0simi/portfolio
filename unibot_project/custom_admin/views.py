from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q

from core.models import (
    Event, Category, FAQ, Favorite, Feedback, CustomUser, KnowledgeBase
)
from .forms import (
    EventForm, CategoryForm, FAQForm, FavoriteForm, FeedbackForm, UserForm, KnowledgeBaseForm
)

def _paginate(request, qs, per_page=12):
    p = Paginator(qs, per_page)
    page = request.GET.get("page") or 1
    return p.get_page(page)

def _search(qs, query, fields):
    if not query:
        return qs
    q_obj = Q()
    for f in fields:
        q_obj |= Q(**{f"{f}__icontains": query})
    return qs.filter(q_obj)

@staff_member_required
def dashboard(request):
    stats = {
        "events": Event.objects.count(),
        "faqs": FAQ.objects.count(),
        "users": CustomUser.objects.count(),
    }
    latest_events = Event.objects.order_by("-start_date")[:5]
    latest_faqs = FAQ.objects.order_by("-updated_at")[:5]
    return render(request, "custom_admin/dashboard.html", {
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
        "title": "لوحة التحكم | UniBot",
    })

# ===== Events =====
@staff_member_required
def event_list(request):
    q = request.GET.get("q")
    qs = Event.objects.order_by("-start_date")
    qs = _search(qs, q, ["title", "location", "description", "slug"])
    page = _paginate(request, qs)
    columns = [("العنوان","title"),("البدء","start_date"),("المكان","location"),("الرابط النظيف","slug")]
    return render(request, "custom_admin/list.html", {
        "title":"الأحداث","create_url":"custom_admin:events_create",
        "edit_url_name":"custom_admin:events_edit","delete_url_name":"custom_admin:events_delete",
        "page_obj":page,"columns":columns,"search_placeholder":"ابحث في العنوان/الوصف/المكان…",
    })

@staff_member_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(); messages.success(request,"تم إنشاء الحدث بنجاح.")
            return redirect("custom_admin:events_list")
    else:
        form = EventForm()
    return render(request, "custom_admin/form.html", {"title":"إضافة حدث","form":form,"back_url":"custom_admin:events_list"})

@staff_member_required
def event_edit(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save(); messages.success(request,"تم تحديث الحدث.")
            return redirect("custom_admin:events_list")
    else:
        form = EventForm(instance=obj)
    return render(request, "custom_admin/form.html", {"title":"تعديل حدث","form":form,"back_url":"custom_admin:events_list"})

@staff_member_required
def event_delete(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف الحدث.")
        return redirect("custom_admin:events_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف حدث","object":obj,"back_url":"custom_admin:events_list"})

# ===== Categories =====
@staff_member_required
def category_list(request):
    q = request.GET.get("q")
    qs = Category.objects.order_by("name")
    qs = _search(qs, q, ["name"])
    page = _paginate(request, qs)
    columns = [("الاسم","name"),("تاريخ الإنشاء","created_at")]
    return render(request, "custom_admin/list.html", {
        "title":"الفئات","create_url":"custom_admin:categories_create",
        "edit_url_name":"custom_admin:categories_edit","delete_url_name":"custom_admin:categories_delete",
        "page_obj":page,"columns":columns,"search_placeholder":"ابحث بالاسم…",
    })

@staff_member_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(); messages.success(request,"تم إضافة الفئة.")
            return redirect("custom_admin:categories_list")
    else:
        form = CategoryForm()
    return render(request, "custom_admin/form.html", {"title":"إضافة فئة","form":form,"back_url":"custom_admin:categories_list"})

@staff_member_required
def category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save(); messages.success(request,"تم تحديث الفئة.")
            return redirect("custom_admin:categories_list")
    else:
        form = CategoryForm(instance=obj)
    return render(request, "custom_admin/form.html", {"title":"تعديل فئة","form":form,"back_url":"custom_admin:categories_list"})

@staff_member_required
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف الفئة.")
        return redirect("custom_admin:categories_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف فئة","object":obj,"back_url":"custom_admin:categories_list"})

# ===== FAQs =====
@staff_member_required
def faq_list(request):
    q = request.GET.get("q")
    qs = FAQ.objects.select_related("category","updated_by").order_by("-updated_at")
    qs = _search(qs, q, ["question","answer","category__name"])
    page = _paginate(request, qs)
    columns = [("السؤال","question"),("الفئة","category"),("آخر تحديث","updated_at")]
    return render(request, "custom_admin/list.html", {
        "title":"الأسئلة الشائعة","create_url":"custom_admin:faqs_create",
        "edit_url_name":"custom_admin:faqs_edit","delete_url_name":"custom_admin:faqs_delete",
        "page_obj":page,"columns":columns,"search_placeholder":"ابحث في السؤال/الإجابة/الفئة…",
    })

@staff_member_required
def faq_create(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.updated_by = request.user
            faq.save(); messages.success(request,"تم إضافة السؤال.")
            return redirect("custom_admin:faqs_list")
    else:
        form = FAQForm()
    return render(request, "custom_admin/form.html", {"title":"إضافة سؤال","form":form,"back_url":"custom_admin:faqs_list"})

@staff_member_required
def faq_edit(request, pk):
    obj = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        form = FAQForm(request.POST, instance=obj)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.updated_by = request.user
            faq.save(); messages.success(request,"تم تحديث السؤال.")
            return redirect("custom_admin:faqs_list")
    else:
        form = FAQForm(instance=obj)
    return render(request, "custom_admin/form.html", {"title":"تعديل سؤال","form":form,"back_url":"custom_admin:faqs_list"})

@staff_member_required
def faq_delete(request, pk):
    obj = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف السؤال.")
        return redirect("custom_admin:faqs_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف سؤال","object":obj,"back_url":"custom_admin:faqs_list"})

# ===== Favorites =====
@staff_member_required
def favorite_list(request):
    q = request.GET.get("q")
    qs = Favorite.objects.select_related("user","faq").order_by("-created_at")
    qs = _search(qs, q, ["user__email","faq__question"])
    page = _paginate(request, qs)
    columns = [("المستخدم","user"),("السؤال","faq"),("تاريخ الإضافة","created_at")]
    return render(request, "custom_admin/list.html", {
        "title":"المفضلات","page_obj":page,"columns":columns,
        "delete_url_name":"custom_admin:favorites_delete","hide_create":True,"edit_url_name":None,
        "search_placeholder":"ابحث بالمستخدم/السؤال…",
    })

@staff_member_required
def favorite_delete(request, pk):
    obj = get_object_or_404(Favorite, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف العنصر من المفضلة.")
        return redirect("custom_admin:favorites_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف مفضلة","object":obj,"back_url":"custom_admin:favorites_list"})

# ===== Feedback =====
@staff_member_required
def feedback_list(request):
    q = request.GET.get("q")
    qs = Feedback.objects.select_related("faq","user").order_by("-created_at")
    qs = _search(qs, q, ["faq__question","user__email","comment"])
    page = _paginate(request, qs)
    columns = [("السؤال","faq"),("المستخدم","user"),("مفيد؟","helpful"),("التعليق","comment"),("التاريخ","created_at")]
    return render(request, "custom_admin/list.html", {
        "title":"التعليقات","page_obj":page,"columns":columns,
        "delete_url_name":"custom_admin:feedback_delete","hide_create":True,"edit_url_name":None,
        "search_placeholder":"ابحث بالسؤال/المستخدم/التعليق…",
    })

@staff_member_required
def feedback_delete(request, pk):
    obj = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف التعليق.")
        return redirect("custom_admin:feedbacks_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف تعليق","object":obj,"back_url":"custom_admin:feedbacks_list"})

# ===== Users =====
@staff_member_required
def user_list(request):
    q = request.GET.get("q")
    qs = CustomUser.objects.order_by("-created_at")
    qs = _search(qs, q, ["email","name","role"])
    page = _paginate(request, qs)
    columns = [("البريد","email"),("الاسم","name"),("الدور","role"),("نشط؟","is_active")]
    return render(request, "custom_admin/list.html", {
        "title":"المستخدمون","create_url":"custom_admin:users_create",
        "edit_url_name":"custom_admin:users_edit","delete_url_name":"custom_admin:users_delete",
        "page_obj":page,"columns":columns,"search_placeholder":"ابحث بالبريد/الاسم/الدور…",
    })

@staff_member_required
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save(); messages.success(request,"تم إنشاء المستخدم.")
            return redirect("custom_admin:users_list")
    else:
        form = UserForm()
    return render(request, "custom_admin/form.html", {"title":"إضافة مستخدم","form":form,"back_url":"custom_admin:users_list"})

@staff_member_required
def user_edit(request, pk):
    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save(); messages.success(request,"تم تحديث المستخدم.")
            return redirect("custom_admin:users_list")
    else:
        form = UserForm(instance=obj)
    return render(request, "custom_admin/form.html", {"title":"تعديل مستخدم","form":form,"back_url":"custom_admin:users_list"})

@staff_member_required
def user_delete(request, pk):
    obj = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف المستخدم.")
        return redirect("custom_admin:users_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف مستخدم","object":obj,"back_url":"custom_admin:users_list"})

# ===== Knowledge Base =====
@staff_member_required
def kb_list(request):
    q = request.GET.get("q")
    qs = KnowledgeBase.objects.order_by("-updated_at")
    qs = _search(qs, q, ["title"])
    page = _paginate(request, qs)
    columns = [("العنوان","title"),("الملف","file"),("آخر تحديث","updated_at")]
    return render(request, "custom_admin/list.html", {
        "title":"Knowledge bases","create_url":"custom_admin:kb_upload",
        "edit_url_name":None,"delete_url_name":"custom_admin:kb_delete",
        "page_obj":page,"columns":columns,"search_placeholder":"ابحث بالعنوان…",
    })

@staff_member_required
def kb_upload(request):
    if request.method == "POST":
        form = KnowledgeBaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(); messages.success(request,"تم رفع الملف.")
            return redirect("custom_admin:kb_list")
    else:
        form = KnowledgeBaseForm()
    return render(request, "custom_admin/form.html", {"title":"رفع ملف معرفة","form":form,"back_url":"custom_admin:kb_list"})

@staff_member_required
def kb_delete(request, pk):
    obj = get_object_or_404(KnowledgeBase, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request,"تم حذف الملف.")
        return redirect("custom_admin:kb_list")
    return render(request, "custom_admin/delete_confirm.html", {"title":"حذف ملف","object":obj,"back_url":"custom_admin:kb_list"})
