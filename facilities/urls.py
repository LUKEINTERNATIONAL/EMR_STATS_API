from django.contrib import admin
from django.urls import path
from facilities.views import FacilityCreate, FacilityList, FacilityDetail, ViralLoadStatus

urlpatterns = [
    path('list/', FacilityList.as_view()),
    path('<int:pk>',FacilityDetail.as_view()),
    path('update_viral_load', ViralLoadStatus.as_view()),
]
