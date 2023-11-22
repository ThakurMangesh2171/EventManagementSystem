from django.urls import path
from .views import create_event,create_user

urlpatterns = [
    path('create_event', create_event, name='create_event'),
    path('create_user', create_user, name='create_user'),
    # path('get_events/', get_events, name='get_events'),
    # Add more URL patterns for other views
]