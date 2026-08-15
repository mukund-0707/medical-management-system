"""
URL routes for Authentication module.
Mounted at: /api/v1/auth/
"""

from django.urls import path
from .views import LoginView, LogoutView, TokenRefreshView, MeView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', MeView.as_view(), name='me'),
]
