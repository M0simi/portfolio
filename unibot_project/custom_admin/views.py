from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from core.models import Event, FAQ, CustomUser

# إن كنت تريد السماح لأي مستخدم مسجّل دخول:
# from django.contrib.auth.decorators import login_required
# @login_required
# def dashboard(request): ...

@staff_member_required
def dashboard(request):
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
