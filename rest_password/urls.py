from django.urls import path
from .views import PasswordResetAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    path('password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    # Add other URL patterns if needed
]