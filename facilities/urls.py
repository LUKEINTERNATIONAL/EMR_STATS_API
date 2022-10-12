from django.contrib import admin
from django.urls import path
from facilities.views import FacilityCreate, FacilityList, FacilityDetail, SiteCreate

urlpatterns = [
    path('',FacilityCreate.as_view()),
    path('create_site',SiteCreate.as_view()),
    path('list/', FacilityList.as_view()),
    path('<int:pk>',FacilityDetail.as_view())
]
