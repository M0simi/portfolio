from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    # Categories CRUD
    path("dashboard/categories/", views.categories_list, name="categories_list"),
    path("dashboard/categories/add/", views.category_add, name="category_add"),
    path("dashboard/categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("dashboard/categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # FAQs CRUD
    path("dashboard/faqs/", views.faqs_list, name="faqs_list"),
    path("dashboard/faqs/add/", views.faq_add, name="faq_add"),
    path("dashboard/faqs/<int:pk>/edit/", views.faq_edit, name="faq_edit"),
    path("dashboard/faqs/<int:pk>/delete/", views.faq_delete, name="faq_delete"),

    # Events
    path("dashboard/events/", views.events_list, name="events_list"),
    path("dashboard/events/add/", views.event_add, name="event_add"),
    path("dashboard/events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("dashboard/events/<int:pk>/delete/", views.event_delete, name="event_delete"),

    # Favorites
    path("dashboard/favorites/", views.favorites_list, name="favorites_list"),
    path("dashboard/favorites/<int:pk>/delete/", views.favorite_delete, name="favorite_delete"),

    # Feedback
    path("dashboard/feedback/", views.feedback_list, name="feedback_list"),
    path("dashboard/feedback/<int:pk>/delete/", views.feedback_delete, name="feedback_delete"),

    # Knowledge bases
    path("dashboard/knowledge/", views.kb_list, name="knowledgebases_list"),
    path("dashboard/knowledge/add/", views.kb_add, name="kb_add"),
    path("dashboard/knowledge/<int:pk>/delete/", views.kb_delete, name="kb_delete"),
]
