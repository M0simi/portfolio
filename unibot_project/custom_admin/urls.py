from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Events
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_add, name="event_add"),

    # Categories / FAQs / Favorites / Feedback / Users / Knowledge
    path("categories/", views.categories_list, name="categories_list"),
    path("faqs/", views.faqs_list, name="faqs_list"),
    path("favorites/", views.favorites_list, name="favorites_list"),
    path("feedback/", views.feedback_list, name="feedback_list"),
    path("users/", views.users_list, name="users_list"),
    path("knowledge/", views.knowledgebases_list, name="knowledgebases_list"),
]
