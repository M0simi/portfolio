from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from core.models import Event, FAQ, CustomUser

@staff_member_required
def dashboard(request):
    # كل شيء داخل try عشان أي خطأ بالكويري ما يطيح الصفحة
    try:
        events_count = Event.objects.count()
    except Exception:
        events_count = 0

    try:
        faqs_count = FAQ.objects.count()
    except Exception:
        faqs_count = 0

    try:
        users_count = CustomUser.objects.count()
    except Exception:
        users_count = 0

    stats = {
        "events_count": events_count,
        "faqs_count": faqs_count,
        "users_count": users_count,
    }

    # أخلي القوائم فاضية مؤقتًا لتجنب أي خطأ تمبليت/علاقات
    latest_events = []
    latest_faqs = []

    return render(request, "custom_admin/dashboard.html", {
        "title": "لوحة التحكّم | UniBot",
        "stats": stats,
        "latest_events": latest_events,
        "latest_faqs": latest_faqs,
    })
