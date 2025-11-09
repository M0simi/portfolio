from django.urls import path
from .views import (
    CustomLoginView,
    get_events,
    search_faqs,
    api_root,
    register_user,
    ai_general,
    get_profile,
    get_event_detail,
)

urlpatterns = [
    path('', api_root, name='api_root'),

    # Auth
    path('login',  CustomLoginView.as_view(), name='login_noslash'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register',  register_user, name='register_user_noslash'),
    path('register/', register_user, name='register_user'),

    # Events
    path('events',  get_events, name='events_noslash'),
    path('events/', get_events, name='events'),
    path('events/<slug:slug>',  get_event_detail, name='event_detail_noslash'),
    path('events/<slug:slug>/', get_event_detail, name='event_detail'),

    # Search & AI
    path('search',  search_faqs, name='search_noslash'),
    path('search/', search_faqs, name='search'),
    path('ai/general',  ai_general, name='ai_general_noslash'),
    path('ai/general/', ai_general, name='ai_general'),

    # Profile
    path('profile',  get_profile, name='get_profile_noslash'),
    path('profile/', get_profile, name='get_profile'),
]
