from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # API 
    path("api/", include("core.urls")),

    # dashboard
    
    path("", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),
  
]

# media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



