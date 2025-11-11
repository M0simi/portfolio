from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard_alt"),
    # Events
    path("events/", views.event_list, name="events_list"),
    path("events/add/", views.event_create, name="events_create"),
    path("events/<str:pk>/edit/", views.event_edit, name="events_edit"),
    path("events/<str:pk>/delete/", views.event_delete, name="events_delete"),

    # Categories
    path("categories/", views.category_list, name="categories_list"),
    path("categories/add/", views.category_create, name="categories_create"),
    path("categories/<str:pk>/edit/", views.category_edit, name="categories_edit"),
    path("categories/<str:pk>/delete/", views.category_delete, name="categories_delete"),

    # FAQs
    path("faqs/", views.faq_list, name="faqs_list"),
    path("faqs/add/", views.faq_create, name="faqs_create"),
    path("faqs/<str:pk>/edit/", views.faq_edit, name="faqs_edit"),
    path("faqs/<str:pk>/delete/", views.faq_delete, name="faqs_delete"),

    # Favorites (عرض + حذف)
    path("favorites/", views.favorite_list, name="favorites_list"),
    path("favorites/<str:pk>/delete/", views.favorite_delete, name="favorites_delete"),

    # Feedback (عرض + حذف)
    path("feedback/", views.feedback_list, name="feedbacks_list"),
    path("feedback/<str:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    # Users
    path("users/", views.user_list, name="users_list"),
    path("users/add/", views.user_create, name="users_create"),
    path("users/<str:pk>/edit/", views.user_edit, name="users_edit"),
    path("users/<str:pk>/delete/", views.user_delete, name="users_delete"),

    # Knowledge Base
    path("kb/", views.kb_list, name="kb_list"),
    path("kb/upload/", views.kb_upload, name="kb_upload"),
    path("kb/<str:pk>/delete/", views.kb_delete, name="kb_delete"),
]
