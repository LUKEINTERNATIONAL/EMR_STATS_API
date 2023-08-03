from django.shortcuts import render
from trackusers.models import TrackUsers
# from encounters.views import RemoteEncounters
from trackusers.serializer import TrackUserSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from users.custom_permissions import CustomPermissionMixin
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse

import pytz
import os
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
timezone = pytz.timezone('Africa/Blantyre')
from services import services
# Create your views here.
class TrackUsersList(CustomPermissionMixin,APIView):
    pass

class TrackUsersDetails(APIView):
    def post(self,request):
      
        login_page = request.POST['login_page']
        other_page = request.POST['other_page']

        try:
           trackuser_results = TrackUsers.objects.get(created_at__date=datetime.today().strftime('%Y-%m-%d'),user_id = request.user.id)
        except TrackUsers.DoesNotExist:
            trackuser_results = False

        if(login_page == 'true'):
            self.process_login_page(request.user.id,trackuser_results)
        elif(other_page == 'true'):
            self.process_other_page(request.user.id,trackuser_results)

        trackuser_results =TrackUsers.objects.get(created_at__date=datetime.today().strftime('%Y-%m-%d'),user_id = request.user.id)
        return JsonResponse({
            'track_users':{
                "login_time":trackuser_results.login_time,
                "logout_time":trackuser_results.logout_time
            }
        })

    def process_login_page(self,user_id,trackuser_results):
        if(trackuser_results):
            login_time = services.get_new_start_datetime(trackuser_results.login_time,trackuser_results.logout_time)
            trackuser_results.login_time = login_time
            trackuser_results.logout_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            trackuser_results.save()
        else:
            data = {
                'user' : user_id,
                'login_time' : datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S'),
                'logout_time' : datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            }
            serializer = TrackUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
    def process_other_page(self,user_id,trackuser_results):
        if(trackuser_results):
            
            time_different = services.get_time_different_in_minutes(trackuser_results.logout_time,datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S'))
            if(time_different < 3):
                trackuser_results.logout_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
                trackuser_results.save()
            else:
                self.process_login_page(user_id,trackuser_results)
        else:
            self.process_login_page(user_id,trackuser_results)

      