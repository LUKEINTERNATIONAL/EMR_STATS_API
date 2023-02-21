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
from vpn_temp.views import VPNTempDetail
from sms.views import SMSDetails
from emails.views import EmailDetails

service = ApplicationService()
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
# Create your views here.
sms = SMSDetails()
email =EmailDetails()
class MessageService(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_staff_message_data(self):
        query ='''  SELECT email,phone,STRING_AGG(facility_name, ', ') AS facilities FROM users_customuser u 
                    INNER JOIN facilities f on f.district_id = u.district_id
                    INNER JOIN vpn v on v.facility_id = f.id
                    WHERE vpn_sms_status ='inactive' AND date = '{}'
                    GROUP BY f.district_id,phone,email; 
            '''.format(datetime.today().strftime('%Y-%m-%d'))
        return service.query_processor(query)
    
    def get_admin_facilities_data(self):
        query ='''  SELECT STRING_AGG(DISTINCT facility_name, ', ') AS facilities FROM users_customuser u 
                    INNER JOIN facilities f on f.district_id = u.district_id
                    INNER JOIN vpn v on v.facility_id = f.id
                    WHERE vpn_sms_status ='inactive' AND date = '{}'; 
            '''.format(datetime.today().strftime('%Y-%m-%d'))
        return service.query_processor(query)
 
    def send_messages(self):
        vpn_tmp =VPNTempDetail()
        vpn_tmp.update_vpn_temp_status()
        self.send_admin_messages()
        self.send_staff_messages()
        VPNTemp.objects.all().delete()

    def send_admin_messages(self):
        query =''' SELECT * FROM users_customuser WHERE is_superuser = 'true'; '''
        user_results = service.query_processor(query)
        facilities = self.get_admin_facilities_data()
        for user in user_results:
            sms_arr =sms.process_sms_messages(facilities[0]['facilities'])
            sms.compose_sms_message(sms_arr,user['phone'])
            message = email.compose_email_message(facilities[0]['facilities'])
            email.send_email(user['email'],message)
           
    def send_staff_messages(self):
        user_results = self.get_staff_message_data()
        for user in user_results:
            sms_arr =sms.process_sms_messages(user['facilities'])
            sms.compose_sms_message(sms_arr,user['phone'])
            message = email.compose_email_message(user['facilities'])
            email.send_email(user['email'],message)

   
