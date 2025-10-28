import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unibot_backend.settings')  # unibot_backend.settings (Key Fix)

application = get_wsgi_application()
