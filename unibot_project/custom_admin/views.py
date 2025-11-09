# custom_admin/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

# لو عندك الموديلات متاحة نستفيد منها في الداشبورد فقط
try:
    from core.models import Event, FAQ, CustomUser
except Exception:
    Event = FAQ = CustomUser = None

# ===== Helpers =====
def _ok(name: str) -> HttpResponse:
    # رد بسيط مؤقت يمنع 500 إلى أن نربط الفورمات/القوالب لاحقًا
    return HttpResponse(f"{name} — سيتم تفعيلها قريبًا ✓", content_type="text/plain; charset=utf-8")

# ===== Dashboard =====
@staff_member_required
def dashboard(request):
    # أرقام آمنة حتى لو فشلت الاستعلامات
    try:
        events_count = Event.objects.count() if Event else 0
    except Exception:
        events_count = 0

    try:
        faqs_count = FAQ.objects.count() if FAQ else 0
    except Exception:
        faqs_count = 0

    try:
        users_count = CustomUser.objects.count() if CustomUser else 0
    except Exception:
        users_count = 0

    stats = {
        "events_count": events_count,
        "faqs_count": faqs_count,
        "users_count": users_count,
    }

    # مؤقتًا نخلي القوائم فاضية لتفادي أي أخطاء تمبليت
    latest_events = []
    latest_faqs = []

    return render(request, "custom_admin/dashboard.html", {
        "title": "لوحة التحكّم | UniBot",
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
    })

# ===== Events =====
@staff_member_required
def event_list(request):        return _ok("قائمة الأحداث")
@staff_member_required
def event_create(request):      return _ok("إضافة حدث")
@staff_member_required
def event_edit(request, pk):    return _ok(f"تعديل حدث #{pk}")
@staff_member_required
def event_delete(request, pk):  return _ok(f"حذف حدث #{pk}")

# ===== Categories =====
@staff_member_required
def category_list(request):        return _ok("قائمة الفئات")
@staff_member_required
def category_create(request):      return _ok("إضافة فئة")
@staff_member_required
def category_edit(request, pk):    return _ok(f"تعديل فئة #{pk}")
@staff_member_required
def category_delete(request, pk):  return _ok(f"حذف فئة #{pk}")

# ===== FAQs =====
@staff_member_required
def faq_list(request):        return _ok("قائمة الأسئلة الشائعة")
@staff_member_required
def faq_create(request):      return _ok("إضافة سؤال")
@staff_member_required
def faq_edit(request, pk):    return _ok(f"تعديل سؤال #{pk}")
@staff_member_required
def faq_delete(request, pk):  return _ok(f"حذف سؤال #{pk}")

# ===== Favorites =====
@staff_member_required
def favorite_list(request):        return _ok("قائمة المفضلات")
@staff_member_required
def favorite_delete(request, pk):  return _ok(f"حذف مفضلة #{pk}")

# ===== Feedbacks =====
@staff_member_required
def feedback_list(request):        return _ok("قائمة التعليقات")
@staff_member_required
def feedback_delete(request, pk):  return _ok(f"حذف تعليق #{pk}")

# ===== Users =====
@staff_member_required
def user_list(request):        return _ok("قائمة المستخدمين")
@staff_member_required
def user_create(request):      return _ok("إضافة مستخدم")
@staff_member_required
def user_edit(request, pk):    return _ok(f"تعديل مستخدم #{pk}")
@staff_member_required
def user_delete(request, pk):  return _ok(f"حذف مستخدم #{pk}")

# ===== Knowledge Base =====
@staff_member_required
def kb_list(request):        return _ok("قائمة ملفات المعرفة")
@staff_member_required
def kb_upload(request):      return _ok("رفع ملف معرفة")
@staff_member_required
def kb_delete(request, pk):  return _ok(f"حذف ملف معرفة #{pk}")
