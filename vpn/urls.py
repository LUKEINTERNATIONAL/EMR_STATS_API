from django.contrib import admin
from django.urls import path
from vpn.views import  VPNList,VPNDetail,VPNCreate,VPNStatus,InternetStatus

urlpatterns = [
    path('', VPNCreate.as_view()),
    path('list/', VPNList.as_view()),
    path('<int:pk>', VPNDetail.as_view()),
    path('vpn_status', VPNStatus.as_view()),
    path('internet_status', InternetStatus.as_view()),

    # get_all_daily_encounters
]
