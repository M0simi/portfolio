# unibot_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # لوحتك المخصّصة تكون على الجذر وعلى /dashboard/ أيضاً
    path("", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),

    # خلي صفحة أدمن دجانغو موجودة (الميدلوير بيحوّل /admin إلى لوحتك)
    path("admin/", admin.site.urls),

    
]
