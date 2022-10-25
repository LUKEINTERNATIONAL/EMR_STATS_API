from django.contrib import admin
from django.urls import path
from encounters.views import EcounterCreate, SiteCreate, EncounterList

urlpatterns = [
    path('',EcounterCreate.as_view()),
    path('create_site',SiteCreate.as_view()),
    path('list/', EncounterList.as_view()),
    # get_all_daily_encounters
]
