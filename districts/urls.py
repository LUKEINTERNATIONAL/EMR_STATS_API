from django.contrib import admin
from django.urls import path
from districts.views import DistrictCreate, DistrictList, DistrictDetail

urlpatterns = [
    path('list/', DistrictList.as_view()),
    path('<int:pk>',DistrictDetail.as_view()),
    path('create_district',DistrictCreate.as_view()),
]
