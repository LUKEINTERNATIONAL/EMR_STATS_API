from django.contrib import admin
from django.urls import path
from databases.views import DatabaseCreate, DatabaseList

urlpatterns = [
    path('',DatabaseCreate.as_view()),
    path('list/', DatabaseList.as_view()),
    # get_all_daily_encounters
]
