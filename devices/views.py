from django.shortcuts import render
from devices.models import Device
from devices.models import DeviceServices
# from encounters.views import RemoteEncounters
from devices.serializer import DeviceSerializer
from devices.serializer import DeviceServicesSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions
from scapy.all import ARP, Ether, srp
import subprocess
from services.remote_operations import RemoteOperations
import re
import ipaddress
import os

# Create your views here.
class FacilityList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT d.id as district_id,f.id as facility_id,* FROM vpn v 
        INNER JOIN devices f on f.id = v.facility_id
        INNER JOIN district d on f.district_id = d.id
        INNER JOIN zone z on d.zone_id = z.id 
        WHERE date = '{}';'''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'devices':results
        })
    
# Create your views here.
class Devices(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM device where facility_id = {};'''.format(request.GET['facility_id'])
        results = service.query_processor(query)
        return JsonResponse({
            'devices':results
        })
    
class DevicesService(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM device_services where device_ip = '{}' ;'''.format(request.GET['ip_address'])
        results = service.query_processor(query)
        return JsonResponse({
            'devices':results
        })
    
class OneFacilityData(APIView):
    def get(self,request,facility_id,start_date,end_date):
        service = ApplicationService()
        query ='''SELECT d.id as district_id,*  FROM encounters e
                INNER JOIN vpn v ON e.encounter_date = v.date
                INNER JOIN devices f on f.id = v.facility_id
                INNER JOIN district d on f.district_id = d.id
                INNER JOIN zone z on d.zone_id = z.id
                WHERE 
                encounter_date BETWEEN {} AND {}
                AND e.facility_id = {} AND v.facility_id = {}
                order by encounter_date;'''.format(start_date,end_date,facility_id,facility_id)
        results = service.query_processor(query)
        return JsonResponse({
            'devices':results
        })
class CreateDevice(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
        
class RemoteDevice(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def process_device(self,data,device_ip,mac_address):
        try:
            exisiting_device = Device.objects.get(device_ip=device_ip,device_mac=mac_address)
        except Device.DoesNotExist:
            exisiting_device =False
        if(exisiting_device):
            self.update_device(data,exisiting_device)
        else:
            self.save_device(data)
        
    def process_device_service(self,data,device_ip,port):
        try:
            exisiting_device = DeviceServices.objects.get(device_ip=device_ip,port=port)
        except DeviceServices.DoesNotExist:
            exisiting_device =False

        if(exisiting_device):
            self.update_device_service(data,exisiting_device)
        else:
            self.save_device_service(data)

    def parse_nmap_scan(self, scan_report,facility_id,ip_address):
        ip_pattern = r'Nmap scan report for ([\d.]+)'
        port_pattern = r'(\d+)/tcp\s+(open|closed|filtered)\s+(\w+)'
        mac_pattern = r'MAC Address:\s+([\w:]+)\s+\((.*?)\)'
        
        current_ip = ''
        print("========================== Devices Found After Scaning ===========================")
        for line in scan_report:
            print(line)
            port_match = re.findall(port_pattern, line)
            mac_match = re.search(mac_pattern, line)

            if line.startswith('Nmap scan report for'):
                current_ip = re.findall(ip_pattern, line)[0]
                if current_ip == ip_address:
                    result = {
                    'facility': facility_id,
                    'device_ip': current_ip,
                    'device_mac': '',
                    'device_status': 'active',
                    'device_name': 'EMR Server'
                    }
                    self.process_device(result,current_ip,'')
            
            if mac_match:
                result = {
                    'facility': facility_id,
                    'device_ip': current_ip,
                    'device_status': 'active',
                    'device_mac': mac_match.group(1) ,
                    'device_name': mac_match.group(2)
                }
                self.process_device(result,current_ip,mac_match.group(1))
            
            if port_match:
                port, state, service_name = port_match[0]
                result = {
                    'device_ip': current_ip,
                    'port': int(port),
                    'state': state,
                    'service': service_name
                }
                self.process_device_service(result,current_ip,int(port))
       

    def save_device(self,request):
        serializer = DeviceSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
        
    def save_device_service(self,request):
        serializer = DeviceServicesSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
 
    def update_device_service(self,request,device):
        if device == False:
            return Response({
                'error': 'Device not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceServicesSerializer(device, data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
    def update_device(self,request,device):
        if device == False:
            return Response({
                'error': 'Device not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceSerializer(device, data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get_remote_device(self,client,facility_details,remote,facility_id):
        print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ {facility_details['ip_address']} @@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(len(self.is_nmap_installed(remote,client)))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if(len(self.is_nmap_installed(remote,client)) > 0):
            Device.objects.update(device_status='inactive')
            data ={
                "remote_ip_range" : ipaddress.IPv4Network(facility_details['ip_address'] + '/' + '24', strict=False),
                "password" : facility_details['password']
            }
            
            devices = remote.scan_remote_network(data,client)
            self.parse_nmap_scan(devices,facility_id,facility_details['ip_address'])
        else:
            self.install_nmap(remote,facility_details,client)

    
    def is_nmap_installed(self,remote,client):
        command = "nmap --version"
        try:
            return remote.execute_command(command,client)
        except OSError:
            return []
    
    def install_nmap(self,remote,facility_details,client):
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' /var/www/EMR_STATS_API/bin/nmap-7.94.tar.bz2 {}@{}:~/"
        .format(facility_details['password'],facility_details['user_name'],facility_details['ip_address']))
        command = '''cd ~/ ; tar xf nmap-7.94.tar.bz2 ; cd ~/nmap-7.94 ;
         ./configure ; echo {} | sudo -S make ; echo {} | sudo -S make install'''.format(facility_details['password'],facility_details['password'])
        remote.execute_command(command,client)

    
                        
                        
     

