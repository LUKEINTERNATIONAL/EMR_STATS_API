
from django.shortcuts import render
from facilities.models import Facility
# from encounters.views import RemoteEncounters
from facilities.serializer import FacilitySerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions
from vpn_temp.models import VPNTemp
from vpn.models import VPN
import requests
import json
import numpy as np
import math

service = ApplicationService()
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
# Create your views here.

class SMSDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def process_sms_messages(self,messages_str):
        massage_arr = messages_str.split(',')
        arr = np.array(massage_arr)
        return np.array_split(arr, math.ceil(len(massage_arr)/6))
        
    def compose_sms_message(self,sms_arr,phone):
        for sms_s in sms_arr:
            message = "VPN down at "+','.join(map(str,sms_s))+" for 24 hours"
            data = {
                'phone':phone, 
                'message':message,
                'messageID':1,
                'ipAddress':config_data['sms_url'],
            }
            self.send_sms(data)
    
    def send_sms(self,sms_data):
        requests.post(url = config_data['sms_url'], json = sms_data)


        

