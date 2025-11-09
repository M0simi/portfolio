from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # لوحة التحكم المخصّصة (تظل الصفحة الرئيسية على الداشبورد)
    path("", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),

    # لوحة Django Admin الأصلية (نبقيها)
    path("admin/", admin.site.urls),

    # REST API
    path("api/", include(("core.urls", "core"), namespace="core")),
]

# ميديا أثناء التطوير/أو لو تحتاج تخدمها مباشرة
# (في الإنتاج الأفضل يكون عبر Cloudinary/Storage أو Nginx، لكن هذا السطر ما يضر)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
