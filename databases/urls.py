from django.contrib import admin
from django.urls import path
from databases.views import DumpsOverview,FacilityDumps

urlpatterns = [
    path('list_dumps/', DumpsOverview.as_view()),
    path('list_facility_dumps/<str:facility_name>', FacilityDumps.as_view()),
    # get_all_daily_encounters
]
