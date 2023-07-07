from django.contrib import admin
from django.urls import path
from encounters.views import EncounterList
from services.remote_service import RemoteService

urlpatterns = [
    # path('create_site',RemoteService.as_view()),
    path('list/', EncounterList.as_view()),
    # get_all_daily_encounters
]
