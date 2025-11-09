from django.urls import path
from .views import CustomLoginView, get_profile, get_events, get_event_detail, search_faqs, api_root, ai_general, register_user

urlpatterns = [
    path("", api_root, name="api_root"),
    path("login/",    CustomLoginView.as_view(), name="login"),
    path("register/", register_user,              name="register_user"),
    path("profile/",  get_profile,                name="get_profile"),
    path("events/",   get_events,                 name="events"),
    path("events/<slug:slug>/", get_event_detail, name="event_detail"),
    path("search/",   search_faqs,                name="search"),
    path("ai/general/", ai_general,               name="ai_general"),
]
