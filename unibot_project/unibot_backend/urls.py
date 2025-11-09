from django.urls import path, include
urlpatterns = [
    path("api/", include("core.urls")),   # لا تغيّر المسار
    path("admin/", admin.site.urls),
    path("", include(("custom_admin.urls","custom_admin"), namespace="custom_admin")),
]
