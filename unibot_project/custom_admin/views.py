from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    # نرسل أرقام ثابتة أولاً لتفادي أي مشاكل داتابيس
    stats = {
        "events_count": 0,
        "faqs_count": 0,
        "users_count": 0,
    }
    latest_events = []
    latest_faqs = []
    return render(request, "custom_admin/dashboard.html", {
        "title": "لوحة التحكّم | UniBot",
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
    })
