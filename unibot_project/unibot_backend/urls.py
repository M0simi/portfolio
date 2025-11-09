from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # API (بدون namespace عشان ما يطلب app_name إجباري)
    path("api/", include("core.urls")),

    # Custom dashboard (الرئيسية و /dashboard/)
    path("", include("custom_admin.urls", namespace="custom_admin")),
]

# Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
