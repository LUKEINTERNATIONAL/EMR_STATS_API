from django.contrib import admin
from django.urls import path
from encounters.views import EcounterCreate

urlpatterns = [
    path('',EcounterCreate.as_view()),
    path('list/', EcounterCreate.as_view()),
]
