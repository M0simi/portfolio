import os
from django.core.wsgi import get_wsgi_application
os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

# اضبط إعدادات المشروع
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unibot_backend.settings')  # تأكد من المسار الصحيح

# أنشئ التطبيق أولاً
application = get_wsgi_application()

# --- Auto apply migrations when server starts (for Render) ---
# يشغّل migrate تلقائيًا عند إقلاع السيرفر (بدون تفاعل)
# يقرأ من متغير بيئة AUTO_MIGRATE (افتراضيًا: مفعّل)
try:
    from django.core.management import call_command

    auto_migrate = os.environ.get("AUTO_MIGRATE", "1")  # "1" => مفعّل
    if auto_migrate in ("1", "true", "True", "TRUE"):
        call_command("migrate", interactive=False, verbosity=1)
        print("✅ Auto-migrate ran successfully from wsgi.py")
    else:
        print("ℹ️ AUTO_MIGRATE disabled; skipping migrate in wsgi.py")
except Exception as e:
    # لا نطيّح السيرفر بسبب خطأ بالمايجريشن — نطبع تحذير فقط
    print(f"⚠️ Migration skipped: {e}")
# -------------------------------------------------------------

