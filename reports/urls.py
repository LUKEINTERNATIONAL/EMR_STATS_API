from django.contrib import admin
from django.urls import path
from reports.views import TotalUsabilityReportList, VPNReportList,ViralLoadList,UsabilityReportList,FacilitiesWithCoordinates,TrackSystemUser

urlpatterns = [
    path('total_usability_report/', TotalUsabilityReportList.as_view()),
    path('facilities_with_coordinates/', FacilitiesWithCoordinates.as_view()),
    path('facilities_without_coordinates/', TotalUsabilityReportList.as_view()),
    path('usability_report/', UsabilityReportList.as_view()),
    path('vpn_report/', VPNReportList.as_view()),
    path('track_user_report', TrackSystemUser.as_view()),
    path('viral_load_report/', ViralLoadList.as_view())
]
