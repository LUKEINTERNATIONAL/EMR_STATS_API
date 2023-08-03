from django.shortcuts import render
from rest_framework.views import APIView 
from service import ApplicationService
from django.http import JsonResponse
from datetime import datetime,timedelta
from vpn.models import VPN

from vpn.serializer import VPNSerializer
from rest_framework.response import Response
from rest_framework import status
from users.custom_permissions import CustomPermissionMixin
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
from services import services


remote = RemoteOperations()
# Create your views here.
            
class VPNCreate(CustomPermissionMixin,APIView):
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

class VPNList(CustomPermissionMixin,APIView):
    def get(self,request):
        service = ApplicationService()
        
        query ='''SELECT * FROM vpn v 
        INNER JOIN facilities f on f.id = v.facility_id 
        LEFT JOIN district d on f.district_id = d.id
        LEFT JOIN zone z on d.zone_id = z.id 
        WHERE date = '{}' {}; '''.format(datetime.today().strftime('%Y-%m-%d'),services.current_user_where(request))
        results = service.query_processor(query)
        return JsonResponse({
            'vpn':results
        })
        
class InternetStatus(CustomPermissionMixin,APIView):
    def get(self,request):
        return JsonResponse({
            'internet':"{}".format(remote.ping(config_data['internet']))
        })
        
class VPNStatus(CustomPermissionMixin,APIView):
    def get(self,request):
        return JsonResponse({
            'vpn':"{}".format(remote.ping(config_data['vpn_ip']))
        })

class VPNDetail(CustomPermissionMixin,APIView):
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
    
class RemoteVNP(CustomPermissionMixin,APIView):
    def getBandwidth(self,remote,client,ip_address):
        network_interface = remote.scan_network_interface(ip_address,client)
        interface_name = network_interface[0].strip()
        tran_reci =remote.scan_bandwidth(interface_name,client)
        strip_tran_reci = tran_reci[0].strip()
        return list(map(int, strip_tran_reci.split()))
        
    def insert_vpnTmp(self,vpn_results):
        vpn_temp = VPNTempCreate()
        vpn_temp.post(vpn_results)
         
    def process_vpn(self,facility_id,status,response,bandwidth):
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
            "received_bandwidth" : bandwidth[0],
            "transmitted_bandwidth" : bandwidth[1],
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
                vpn_data['start_down_time'] =services.get_new_start_datetime(vpn_results.start_down_time,vpn_results.end_down_time)
            vpn.put(vpn_data,vpn_results.id)
            print("vpn status updated with downtime")
        else:
            vpn =VPNCreate()
            vpn.post(vpn_data)
            print("vpn status created")
            
    

      


   