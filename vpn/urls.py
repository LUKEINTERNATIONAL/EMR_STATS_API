from django.contrib import admin
from django.urls import path
from vpn.views import  VPNList,VPNDetail,VPNCreate

urlpatterns = [
    path('', VPNCreate.as_view()),
    path('list/', VPNList.as_view()),
    path('<int:pk>', VPNDetail.as_view()),

    # get_all_daily_encounters
]
