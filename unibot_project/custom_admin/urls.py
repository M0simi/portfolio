from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    # dashboard
    path("", views.dashboard, name="dashboard"),

    # events
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_add, name="event_add"),
    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),

    # categories
    path("categories/", views.categories_list, name="categories_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # faqs
    path("faqs/", views.faqs_list, name="faqs_list"),
    path("faqs/add/", views.faq_add, name="faq_add"),
    path("faqs/<int:pk>/edit/", views.faq_edit, name="faq_edit"),
    path("faqs/<int:pk>/delete/", views.faq_delete, name="faq_delete"),

    # favorites
    path("favorites/", views.favorites_list, name="favorites_list"),
    path("favorites/<int:pk>/delete/", views.favorite_delete, name="favorite_delete"),

    # feedback
    path("feedback/", views.feedback_list, name="feedback_list"),
    path("feedback/<int:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    # users
    path("users/", views.users_list, name="users_list"),

    # knowledge bases
    path("knowledge/", views.knowledgebases_list, name="knowledgebases_list"),
    path("knowledge/add/", views.kb_add, name="kb_add"),
    path("knowledge/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
    path("fix/kb/reset/", views.kb_reset, name="kb_reset"),
]
