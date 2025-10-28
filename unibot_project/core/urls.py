from django.urls import path
from .views import (
    CustomLoginView,
    get_events,
    search_faqs,
    api_root,
    register_user,
    ai_general,
    get_profile,  
)

urlpatterns = [
    path('', api_root, name='api_root'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_user, name='register_user'),
    path('events/', get_events, name='events'),
    path('search/', search_faqs, name='search'),
    path('ai/general/', ai_general, name='ai_general'),
    path('profile/', get_profile, name='get_profile'),  
]

