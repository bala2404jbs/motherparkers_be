from django.urls import path
from . import views

from rest_framework.authtoken import views as drf_auth_views
from .views import RegisterView, CustomAuthToken, LogoutView, UserProfileView

urlpatterns = [
    # Registration
    path('register/', RegisterView.as_view(), name='register'),
    # Login (token)
    path('login/', CustomAuthToken.as_view(), name='login'),
    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
]
