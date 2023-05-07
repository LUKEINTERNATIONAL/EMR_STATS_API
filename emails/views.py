
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
from services.tasks import send_sms_email

service = ApplicationService()
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
# Create your views here.

class EmailDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
   
  
    def attachments(self):
        return [
                    {
                    'filename': 'LIN.png',
                    'path': 'LIN.png',
                    'cid': 'LIN@nodemailer.com' 
                    },
                    {
                    'filename': 'mw.png',
                    'path': 'mw.png',
                    'cid': 'mwpng@nodemailer.com'
                    },
                    {
                    'filename': 'egpaf.png',
                    'path': 'egpaf.png',
                    'cid': 'egpaf@nodemailer.com'
                    }
                ]
    

    def process_email_massage(self,facilities_str):
        facilities_data = ''
        facilities = facilities_str.split(',')
        for facility in facilities:
            facilities_data = facilities_data+'''<li class=""><a href="#" style="position: relative;
            display: block;padding: .4em .4em .4em 2em;margin: .5em 0;background: #DAD2CA;
            color: #444;text-decoration: none;border-radius: .3em;transition: .3s ease-out;
            ">{}</a></li>'''.format(facility)
        return facilities_data


    def compose_email_message(self,facilities_str):
        facilities = self.process_email_massage(facilities_str)
        return '''
            <div class="containt" style="width: 90%;margin: auto;">
                <header>
                    <h1 style="font-size: 18px;font-weight: 600; text-align: center;">
                        Facilities with VPN Down for 24 hour ({})
                    </h1>
                </header>
            <ol style="counter-reset: li;list-style: none;padding: 0;text-shadow: 0 1px 0 rgba(255,255,255,.5);">
                <li class="">
                    {}
                </li>
            </ol><div>
            <footer style="position: absolute; bottom: 0; left: 0; right: 0;  background: gainsboro;  height: auto; width: auto; color: #fff; border-radius: 0px; margin-left: 0.5%; margin-top: 1%;">
                <div style="display: flex;  align-items: center; justify-content: center; flex-direction: column; text-align: center;">
                    
                    <h3 style="font-size: 2.1rem; font-weight: 500; text-transform: capitalize; line-height: 3rem;">
                    <!--left blank -->
                    </h3>
                    <div style="margin: 10px auto;">
                        <img src="cid:mwpng@nodemailer.com"/>
                    </div>
                    <div style="margin: 10px auto;">
                        <img src="cid:LIN@nodemailer.com"/>
                    </div>
                    <div style="margin: 10px auto;">
                        <img src="cid:egpaf@nodemailer.com"/>
                    </div>
                </div>
            </footer>
        '''.format(datetime.today().strftime('%Y-%m-%d'),facilities)
        
    def send_email(self,email,message):
        mailOptions = {
            'from': config_data['from_email'],
            'to': email,
            'subject': 'VPN Status Notifications',
            'html': message,
            'attachments': self.attachments()
        }
        message_data = {
            'mailOptions': mailOptions,
            'ipAddress':config_data['base_url'],
            'messageIDs':1
        }
        send_sms_email.delay(config_data['email_url'],message_data,"Email")

        

