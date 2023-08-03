from django.contrib import admin
from django.urls import path
from trackusers.views import TrackUsersDetails

urlpatterns = [
    path('', TrackUsersDetails.as_view()),

    # get_all_daily_encounters
]
