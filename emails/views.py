
from django.shortcuts import render
from facilities.models import Facility
# from encounters.views import RemoteEncounters
from facilities.serializer import FacilitySerializer
from rest_framework.views import APIView 
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from vpn_temp.models import VPNTemp
from vpn.models import VPN
import requests
import json
import numpy as np
import math
from services.tasks import send_sms_email
from users.custom_permissions import CustomPermissionMixin

service = ApplicationService()
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
# Create your views here.

class EmailDetails(CustomPermissionMixin,APIView):
    
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
    

    def compose_password_email(self,name, username,password):
        return '''
            Date: {},<br/><br/>

            Dear {},<br><br>

            I hope this email finds you well. We are delighted to inform you that your account <br>
            has been successfully created in EMR Monitor System.<br><br>

            Your login credentials are as follows:<br>
            Username: {}<br>
            Temporary Password: {}<br><br>

            Note: For security purposes, we highly recommend that you change your password after your first login. <br>
            To do this, simply follow the instructions on the login page and set a strong, unique password.<br><br>
 
            Should you encounter any issues or have any questions, <br>
            please do not hesitate to reach out to our dedicated support team at kayangepetros@gmail.com/265999500312.<br><br>

            To access your account, simply visit our website (http://10.44.0.86:4000/) and use the login credentials provided above.<br>
            Make sure you are connected to VPN when visiting the website.<br><br>

            We look forward to serving you and providing a valuable experience.<br><br>

            Best regards,<br><br>

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
        '''.format(datetime.today().strftime('%Y-%m-%d'),name,username,password)
    
    
        
    def send_email(self,email,message,title):
        mailOptions = {
            'from': config_data['from_email'],
            'to': email,
            'subject': title,
            'html': message,
            'attachments': self.attachments()
        }
        message_data = {
            'mailOptions': mailOptions,
            'ipAddress':config_data['base_url'],
            'messageIDs':1
        }
        send_sms_email.delay(config_data['email_url'],message_data,"Email")

        

