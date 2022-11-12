from django.contrib import admin
from django.urls import path
from reports.views import EncounterReportList, VPNReportList

urlpatterns = [
    path('encounter_report/', EncounterReportList.as_view()),
    path('vpn_report/', VPNReportList.as_view())
]
