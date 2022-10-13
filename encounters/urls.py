from django.contrib import admin
from django.urls import path
from encounters.views import EcounterCreate, SiteCreate

urlpatterns = [
    path('',EcounterCreate.as_view()),
    path('create_site',SiteCreate.as_view()),
    path('list/', EcounterCreate.as_view()),
]
