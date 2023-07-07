from django.contrib import admin
from django.urls import path
from facilities.views import FacilityCreate, FacilityList, FacilityDetail, facilityStatus, OneFacilityData, Facilities

urlpatterns = [
    path('create_facility', FacilityCreate.as_view()),
    path('list/', FacilityList.as_view()),
    path('', Facilities.as_view()),
    path('one_facility_data/<str:facility_id>/<str:start_date>/<str:end_date>', OneFacilityData.as_view()),
    path('<int:pk>',FacilityDetail.as_view()),
    path('update_viral_load', facilityStatus.as_view()),
    path('update_get_device_status', facilityStatus.as_view()),
    path('update_close_mon', facilityStatus.as_view()),
]
