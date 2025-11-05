from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Categories
    path("categories/", views.categories_list, name="categories_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/<uuid:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<uuid:pk>/delete/", views.category_delete, name="category_delete"),

    # FAQ
    path("faqs/", views.faqs_list, name="faqs_list"),
    path("faqs/add/", views.faq_add, name="faq_add"),
    path("faqs/<uuid:pk>/edit/", views.faq_edit, name="faq_edit"),
    path("faqs/<uuid:pk>/delete/", views.faq_delete, name="faq_delete"),

    # Events
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_add, name="event_add"),
    path("events/<uuid:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<uuid:pk>/delete/", views.event_delete, name="event_delete"),

    # KnowledgeBase
    path("kb/", views.kb_list, name="kb_list"),
    path("kb/add/", views.kb_add, name="kb_add"),
    path("kb/<int:pk>/edit/", views.kb_edit, name="kb_edit"),
    path("kb/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
    path("kb/<int:pk>/download/", views.kb_download, name="kb_download"),

    # Feedback / Favorites (عرض فقط)
    path("feedback/", views.feedback_list, name="feedback_list"),
    path("favorites/", views.favorites_list, name="favorites_list"),

    # Users
    path("users/", views.users_list, name="users_list"),
    path("users/<uuid:pk>/edit/", views.user_edit, name="user_edit"),
]
