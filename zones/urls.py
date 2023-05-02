from django.contrib import admin
from django.urls import path
from zones.views import ZoneCreate,ZonesList,ZoneDetail

urlpatterns = [
    path('list/', ZonesList.as_view()),
    path('create_zone',ZoneCreate.as_view()),
    path('<int:pk>',ZoneDetail.as_view()),
]
