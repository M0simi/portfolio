# unibot_backend/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unibot_backend.settings')

application = get_wsgi_application()

# ✅ ضروري: استيراد settings ثم إنشاء مجلد MEDIA
from django.conf import settings
os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

# (اختياري) تطبيق المايجريشن تلقائيًا على Render
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
except Exception as e:
    print(f"⚠️ Migration skipped: {e}")
