from django.contrib import admin
from django.urls import path
from databases.views import DumpsOverview,FacilityDumps,DownloadDump

urlpatterns = [
    path('list_dumps/', DumpsOverview.as_view()),
    path('list_facility_dumps/<str:facility_name>', FacilityDumps.as_view()),
    path('download_dump/<str:dump_name>', DownloadDump.as_view()),
    # get_all_daily_encounters
]
