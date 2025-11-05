from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("events/", views.events_list, name="events_list"),
    path("events/add/", views.event_add, name="event_add"),
]
