from django.contrib import admin
from django.urls import path
from devices.views import OneFacilityData, Devices, OneFacilityData, DevicesService

urlpatterns = [
    path('list/', Devices.as_view()),
    path('list_devices_service', DevicesService.as_view()),
    path('', OneFacilityData.as_view()),
    path('one_facility_data/<str:facility_id>/<str:start_date>/<str:end_date>', OneFacilityData.as_view()),
]
