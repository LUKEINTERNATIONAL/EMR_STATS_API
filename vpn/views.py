from django.shortcuts import render
from rest_framework.views import APIView 
from service import ApplicationService
from django.http import JsonResponse
from datetime import datetime,timedelta
from vpn.models import VPN

from vpn.serializer import VPNSerializer
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from vpn_temp.views import VPNTempCreate
from services.remote_operations import RemoteOperations

import pytz
import os
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
timezone = pytz.timezone('Africa/Blantyre')


remote = RemoteOperations()
# Create your views here.
            
class VPNCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = VPNSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VPNList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM vpn v INNER JOIN facilities f on f.id = v.facility_id 
        WHERE date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'vpn':results
        })
        
class InternetStatus(APIView):
    def get(self,request):
        return JsonResponse({
            'internet':"{}".format(remote.ping(config_data['internet']))
        })
        
class VPNStatus(APIView):
    def get(self,request):
        return JsonResponse({
            'vpn':"{}".format(remote.ping(config_data['vpn_ip']))
        })

class VPNDetail(APIView):
    def get_vpn_by_pk(self,pk):
        try:
            return VPN.objects.get(pk=pk)
        except:
            return Response({
                'error': 'Facility does not exit'
            }, status=status.HTTP_404_NOT_FOUND)
 
    def get(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        serializer = VPNSerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        vpn = self.get_vpn_by_pk(pk)
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = VPNSerializer(vpn, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RemoteVNP(APIView):
    def insert_vpnTmp(self,vpn_results):
        vpn_temp = VPNTempCreate()
        vpn_temp.post(vpn_results)
         
    def process_vpn(self,facility_id,status,response):
        try:
            vpn_results = VPN.objects.get(date=datetime.today().strftime('%Y-%m-%d'), facility_id=facility_id)
        except VPN.DoesNotExist:
            vpn_results = False
            print(f"VPN failed to update or create {facility_id} VPN status = {status}")
        if(not response):
            response = 0.00
            
        vpn_data = {
            "facility": facility_id,
            "start_down_time":datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "end_down_time":datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "response_time" : response,
            "vpn_status" : status,
            "date"       : datetime.today().strftime('%Y-%m-%d')
        }
        self.insert_vpnTmp(vpn_data)
        if vpn_results and vpn_results.vpn_status == 'active':
            vpn =VPNDetail()
            vpn_data.pop('end_down_time')
            vpn_data.pop('start_down_time')
            vpn.put(vpn_data,vpn_results.id)
            print("vpn status updated without downtime")
        elif(vpn_results and vpn_results.vpn_status == 'inactive'):
            vpn =VPNDetail()
            vpn_data['end_down_time'] = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            
            if(vpn_results.vpn_status == status):
                vpn_data.pop('start_down_time')
            else:
                vpn_data['start_down_time'] =self.get_new_start_downtime(vpn_results.start_down_time,vpn_results.end_down_time)
            vpn.put(vpn_data,vpn_results.id)
            print("vpn status updated with downtime")
        else:
            vpn =VPNCreate()
            vpn.post(vpn_data)
            print("vpn status created")
            
    def get_new_start_downtime(self,start_time_str,end_time_str):
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        seconds = (end_time - start_time).total_seconds()
        duration_hours = seconds // 3600
        duration_minutes = (seconds % 3600) // 60
        duration = timedelta(hours=duration_hours, minutes=duration_minutes)
        current_time = datetime.now(timezone)
        end_time = current_time - duration
        return end_time.strftime('%Y-%m-%d %H:%M:%S')

      


   