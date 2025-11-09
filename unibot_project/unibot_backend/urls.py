# unibot_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("admin/", admin.site.urls),

    
    path("", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),

   
    path("api/", include(("core.urls", "core"), namespace="core")),
]


if settings.DEBUG and settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
