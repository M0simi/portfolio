from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# نجرب نستورد الموديلات، ولو صار أي خطأ نخلي القيم صفر
try:
    from core.models import Event, FAQ, CustomUser
except Exception:
    Event = FAQ = CustomUser = None

@staff_member_required
def dashboard(request):
    # أرقام آمنة حتى لو فيه أي مشكلة بالاتصال بالداتا أو الموديلات
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

    # مؤقتًا نخلي القوائم فاضية لتفادي أي أخطاء عرض
    latest_events = []
    latest_faqs = []

    return render(request, "custom_admin/dashboard.html", {
        "title": "لوحة التحكّم | UniBot",
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
    })
