# custom_admin/urls.py
from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Events
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_create, name="events_create"),
    path("events/<int:pk>/edit/", views.event_edit, name="events_edit"),
    path("events/<int:pk>/delete/", views.event_delete, name="events_delete"),

    # Categories
    path("categories/", views.categories_list, name="categories_list"),
    path("categories/add/", views.category_create, name="categories_create"),
    path("categories/<int:pk>/edit/", views.category_edit, name="categories_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="categories_delete"),

    # FAQs
    path("faqs/", views.faqs_list, name="faqs_list"),
    path("faqs/add/", views.faq_create, name="faqs_create"),
    path("faqs/<int:pk>/edit/", views.faq_edit, name="faqs_edit"),
    path("faqs/<int:pk>/delete/", views.faq_delete, name="faqs_delete"),

    # Favorites
    path("favorites/", views.favorites_list, name="favorites_list"),
    path("favorites/<int:pk>/delete/", views.favorite_delete, name="favorites_delete"),

    # Feedbacks
    path("feedbacks/", views.feedbacks_list, name="feedbacks_list"),
    path("feedbacks/<int:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    # Users
    path("users/", views.users_list, name="users_list"),
    path("users/add/", views.user_create, name="users_create"),
    path("users/<int:pk>/edit/", views.user_edit, name="users_edit"),
    path("users/<int:pk>/delete/", views.user_delete, name="users_delete"),

    # Knowledge Bases
    path("knowledge-bases/", views.kb_list, name="kb_list"),
    path("knowledge-bases/upload/", views.kb_upload, name="kb_upload"),
    path("knowledge-bases/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
]
