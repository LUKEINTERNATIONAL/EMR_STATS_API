from django.contrib import admin
from django.urls import path
from zones.views import ZoneCreate,ZonesList

urlpatterns = [
    path('list/', ZonesList.as_view()),
    path('create_zone',ZoneCreate.as_view()),
]
