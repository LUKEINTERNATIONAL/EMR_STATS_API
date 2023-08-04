from django.contrib import admin
from django.urls import path
from change_password.views import PasswordChangeView

urlpatterns = [
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]
