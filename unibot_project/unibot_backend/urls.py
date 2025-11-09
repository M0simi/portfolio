from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path("", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),

    
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
