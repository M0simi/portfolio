# custom_admin/views.py
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.admin.views.decorators import staff_member_required

# ملاحظة: هذه العناوين تفترض أن نماذجك في app اسمها "core"
# غيّر المسارات لو كان app label مختلف

# ===== Dashboard =====
@staff_member_required
def dashboard(request):
    # لوحة مبدئية: نوجّه للـ Admin مباشرة
    return redirect("/admin/")

# ===== Events =====
@staff_member_required
def events_list(request):
    return redirect("/admin/core/event/")

@staff_member_required
def event_add(request):
    return redirect("/admin/core/event/add/")

@staff_member_required
def event_edit(request, pk: int):
    return redirect(f"/admin/core/event/{pk}/change/")

@staff_member_required
def event_delete(request, pk: int):
    return redirect(f"/admin/core/event/{pk}/delete/")

# ===== Categories =====
@staff_member_required
def categories_list(request):
    return redirect("/admin/core/category/")

@staff_member_required
def category_add(request):
    return redirect("/admin/core/category/add/")

@staff_member_required
def category_edit(request, pk: int):
    return redirect(f"/admin/core/category/{pk}/change/")

@staff_member_required
def category_delete(request, pk: int):
    return redirect(f"/admin/core/category/{pk}/delete/")

# ===== FAQs =====
@staff_member_required
def faqs_list(request):
    return redirect("/admin/core/faq/")

@staff_member_required
def faq_add(request):
    return redirect("/admin/core/faq/add/")

@staff_member_required
def faq_edit(request, pk: int):
    return redirect(f"/admin/core/faq/{pk}/change/")

@staff_member_required
def faq_delete(request, pk: int):
    return redirect(f"/admin/core/faq/{pk}/delete/")

# ===== Favorites =====
@staff_member_required
def favorites_list(request):
    return redirect("/admin/core/favorite/")

@staff_member_required
def favorite_delete(request, pk: int):
    return redirect(f"/admin/core/favorite/{pk}/delete/")

# ===== Feedback =====
@staff_member_required
def feedback_list(request):
    return redirect("/admin/core/feedback/")

@staff_member_required
def feedback_delete(request, pk: int):
    return redirect(f"/admin/core/feedback/{pk}/delete/")

# ===== Users =====
@staff_member_required
def users_list(request):
    # اسم الموديل CustomUser ⇒ admin changelist على:
    return redirect("/admin/core/customuser/")

# ===== Knowledge Base =====
@staff_member_required
def knowledgebases_list(request):
    return redirect("/admin/core/knowledgebase/")

@staff_member_required
def kb_add(request):
    return redirect("/admin/core/knowledgebase/add/")

@staff_member_required
def kb_delete(request, pk: int):
    return redirect(f"/admin/core/knowledgebase/{pk}/delete/")

# أداة صيانة اختيارية، حالياً ترجع JSON بسيط (تقدر تطورها لاحقاً)
@staff_member_required
def kb_reset(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    # لاحقاً: ضف منطق التنظيف (مثلاً إبقاء آخر KB وحذف الباقي)
    return JsonResponse({"ok": True, "msg": "KB reset endpoint placeholder"})
