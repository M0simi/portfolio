# custom_admin/urls.py
from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
     # الجذر يفتح الداشبورد
    path("", views.dashboard, name="dashboard"),
    # وقناة احتياطية لو كتبت /dashboard/ يفتح نفس الصفحة
    path("dashboard/", views.dashboard, name="dashboard_explicit"),

    # Events
    path("events/", views.event_list, name="events_list"),
    path("events/create/", views.event_create, name="events_create"),
    path("events/<uuid:pk>/edit/", views.event_edit, name="events_edit"),
    path("events/<uuid:pk>/delete/", views.event_delete, name="events_delete"),

    # Categories
    path("categories/", views.category_list, name="categories_list"),
    path("categories/create/", views.category_create, name="categories_create"),
    path("categories/<uuid:pk>/edit/", views.category_edit, name="categories_edit"),
    path("categories/<uuid:pk>/delete/", views.category_delete, name="categories_delete"),

    # FAQs
    path("faqs/", views.faq_list, name="faqs_list"),
    path("faqs/create/", views.faq_create, name="faqs_create"),
    path("faqs/<uuid:pk>/edit/", views.faq_edit, name="faqs_edit"),
    path("faqs/<uuid:pk>/delete/", views.faq_delete, name="faqs_delete"),

    # Favorites
    path("favorites/", views.favorite_list, name="favorites_list"),
    path("favorites/<uuid:pk>/delete/", views.favorite_delete, name="favorites_delete"),

    # Feedbacks
    path("feedbacks/", views.feedback_list, name="feedbacks_list"),
    path("feedbacks/<uuid:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    # Users
    path("users/", views.user_list, name="users_list"),
    path("users/create/", views.user_create, name="users_create"),
    path("users/<uuid:pk>/edit/", views.user_edit, name="users_edit"),
    path("users/<uuid:pk>/delete/", views.user_delete, name="users_delete"),

    # Knowledge Base
    path("kb/", views.kb_list, name="kb_list"),
    path("kb/upload/", views.kb_upload, name="kb_upload"),
    path("kb/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
]
