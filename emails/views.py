
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

    def footer(self):
        return '''<footer style="padding: 20px 0;">
                    <div style="margin: 0 auto;">
                    <div style="display: flex; justify-content: center;">
                        <ul style="list-style: none; margin: 0; padding: 0; display: flex; align-items: center;" class="logo-list">
                        <li style="margin-right: 20px;"><img src="cid:mwpng@nodemailer.com" height="50"></li>
                        <li style="margin-right: 20px;"><img src="cid:LIN@nodemailer.com" height="50"></li>
                        <li><img src="cid:egpaf@nodemailer.com" height="50"></li>
                        </ul>
                    </div>
                    </div>
                </footer>'''
    
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
            {}
        '''.format(datetime.today().strftime('%Y-%m-%d'),facilities,self.footer())
    

    def compose_password_email(self,name, username,password):
        return '''
            <b>Date:</b> {},<br/><br/>

            <b>Dear</b> {},<br><br>

            I hope this email finds you well. We are delighted to inform you that your account <br>
            has been successfully created in EMR Monitor System.<br><br>

            <b>Your login credentials are as follows </b><br>
            Username:<b> {}<br> </b>
            Temporary Password: <b> {} </b><br><br>

            <b>Note:</b> For security purposes, we highly recommend that you change your password after your first login. <br>
            To do this, simply follow the instructions on the login page and set a strong, unique password.<br><br>
 
            Should you encounter any issues or have any questions, <br>
            please do not hesitate to reach out to our dedicated support team at <br>
                 <b>Email:</b> kayangepetros@gmail.com<br>
                 <b>Phone:</b> +265999500312.<br><br>

            To access your account, simply visit our website (http://10.44.0.86:4000/) and use the login credentials provided above.<br>
            <b>Note:</b> Make sure you are connected to VPN when visiting the website.<br><br>

            We look forward to serving you and providing a valuable experience.<br><br>

            Best regards,<br><br>

            {}
        '''.format(datetime.today().strftime('%Y-%m-%d'),name,username,password,self.footer())
    
    
        
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

        

