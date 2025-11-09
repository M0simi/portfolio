from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # API
    path("api/", include("core.urls", namespace="core")),

    # Custom dashboard (home & /dashboard/)
    path("", include("custom_admin.urls", namespace="custom_admin")),
]

# Media (served by Django; fine on Render for user uploads)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
