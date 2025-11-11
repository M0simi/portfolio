from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# نحاول الاستيراد بدون ما نطيح السيرفر لو في مشاكل
try:
    from core.models import Event, FAQ, CustomUser
except Exception:  # noqa: BLE001
    Event = FAQ = CustomUser = None


@staff_member_required
def dashboard(request):
    events_count = faqs_count = users_count = 0
    latest_events = []
    latest_faqs = []

    if Event:
        try:
            events_count = Event.objects.count()
            latest_events = Event.objects.order_by("-start_date")[:5]
        except Exception:
            pass

    if FAQ:
        try:
            faqs_count = FAQ.objects.count()
            latest_faqs = FAQ.objects.order_by("-updated_at")[:5]
        except Exception:
            pass

    if CustomUser:
        try:
            users_count = CustomUser.objects.count()
        except Exception:
            pass

    stats = {
        "events": events_count,
        "events_count": events_count,
        "faqs": faqs_count,
        "faqs_count": faqs_count,
        "users": users_count,
        "users_count": users_count,
    }

    return render(
        request,
        "custom_admin/dashboard.html",
        {
            "title": "لوحة التحكم | UniBot",
            "stats": stats,
            "latest_events": latest_events,
            "latest_faqs": latest_faqs,
        },
    )
