from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.events_create, name="events_create"),
    path("events/<int:pk>/edit/", views.events_edit, name="events_edit"),
    path("events/<int:pk>/delete/", views.events_delete, name="events_delete"),

    path("categories/", views.categories_list, name="categories_list"),
    path("categories/add/", views.categories_create, name="categories_create"),
    path("categories/<int:pk>/edit/", views.categories_edit, name="categories_edit"),
    path("categories/<int:pk>/delete/", views.categories_delete, name="categories_delete"),

    path("faqs/", views.faqs_list, name="faqs_list"),
    path("faqs/add/", views.faqs_create, name="faqs_create"),
    path("faqs/<int:pk>/edit/", views.faqs_edit, name="faqs_edit"),
    path("faqs/<int:pk>/delete/", views.faqs_delete, name="faqs_delete"),

    path("favorites/", views.favorites_list, name="favorites_list"),
    path("favorites/<int:pk>/delete/", views.favorites_delete, name="favorites_delete"),

    path("feedback/", views.feedback_list, name="feedback_list"),
    path("feedback/<int:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    path("users/", views.users_list, name="users_list"),
    path("users/add/", views.users_create, name="users_create"),
    path("users/<int:pk>/edit/", views.users_edit, name="users_edit"),
    path("users/<int:pk>/delete/", views.users_delete, name="users_delete"),

    path("kb/", views.kb_list, name="kb_list"),
    path("kb/upload/", views.kb_upload, name="kb_upload"),
    path("kb/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
]
