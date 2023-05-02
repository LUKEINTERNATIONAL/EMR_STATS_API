from django.shortcuts import render
from rest_framework.views import APIView 
from service import ApplicationService
from django.http import JsonResponse
from datetime import datetime
from vpn_temp.models import VPNTemp

from vpn_temp.serializer import VPNTempSerializer
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService




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
import os
service = ApplicationService()
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
# Create your views here.


# Create your views here.
class VPNTempCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = VPNTempSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VPNTempList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM vpn_temp v INNER JOIN facilities f on f.id = v.facility_id 
        WHERE date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'vpn_temp':results
        })

class VPNTempDetail(APIView):
    def get_vpn_by_pk(self,pk):
        try:
            return VPNTemp.objects.get(pk=pk)
        except:
            return Response({
                'error': 'Facility does not exit'
            }, status=status.HTTP_404_NOT_FOUND)
 
    def get(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        serializer = VPNTempSerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        VPNTemp = self.get_vpn_by_pk(pk)
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = VPNTempSerializer(VPNTemp, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_vpn_temp_status(self):
        query ='''SELECT * FROM vpn WHERE date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        vpn_results = service.query_processor(query)
        for vpn in vpn_results:
            print(vpn)
            try:
                query ='''SELECT * FROM vpn_temp WHERE DATE(created_at) = '{}' AND vpn_status='active' AND facility_id = '{}'; '''.\
                format(datetime.today().strftime('%Y-%m-%d'),vpn['facility_id'])
                vpn_temp_results = service.query_processor(query)
            except:
                vpn_temp_results = False
            
            if(vpn_temp_results):
                query = '''UPDATE vpn SET vpn_sms_status='active' WHERE id={};'''.format(vpn['id'])
            else:    
                query = ''' UPDATE vpn SET vpn_sms_status='inactive' WHERE id={}; '''.format(vpn['id'])  

            print(f"vpn query {query}")
            try:
                service.query_processor(query)  
            except:
                print("fail to update vpn temp status id = {}".format(vpn['id']))





    


 
           
    

        

