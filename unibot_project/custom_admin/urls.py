from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard_alt"),

    # Events CRUD
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_add, name="event_add"),
    path("events/<uuid:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<uuid:pk>/delete/", views.event_delete, name="event_delete"),
]
