from django.shortcuts import render
from devices.models import Device
# from encounters.views import RemoteEncounters
from devices.serializer import DeviceSerializer
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
class devices(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM devices ;'''
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

    

    def scan_remote_network(self,ip_range):
        # Create an ARP request packet
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)

        # Use sudo to run srp with elevated privileges
        process = subprocess.Popen(['sudo', '-S', 'python', '-c',
                                    'from scapy.all import *; result = srp(arp_request, timeout=3, verbose=0)[0]; print(result)'],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Provide the sudo password if prompted
        process.stdin.write('lin@1088\n')
        process.stdin.flush()

        # Wait for the process to finish and capture the output
        output, error = process.communicate()
        print(error)

        devices = []
        lines = output.split('\n')
        for line in lines:
            if line.startswith('Begin emission'):
                # Start parsing the received packets
                while True:
                    line = next(lines)
                    if line.startswith('End emission'):
                        break
                    elif line.startswith('Received '):
                        parts = line.split()
                        ip, mac = parts[1], parts[4]
                        devices.append({'ip': ip, 'mac': mac})

        return devices
    

    def parse_nmap_scan(self, scan_report):
        ip_pattern = r'Nmap scan report for ([\d.]+)'
        port_pattern = r'(\d+)/tcp\s+(open|closed|filtered)\s+(\w+)'
        mac_pattern = r'MAC Address:\s+([\w:]+)\s+\((.*?)\)'
        
        results = []
        port_details = []
        current_ip = None
        for line in scan_report:
            if line.startswith('Nmap scan report for'):
                current_ip = re.findall(ip_pattern, line)[0]
            else:
                port_match = re.findall(port_pattern, line)
                mac_match = re.search(mac_pattern, line)
                if port_match:
                    port, state, service_name = port_match[0]
                    result = {
                        'ip': current_ip,
                        'port': int(port),
                        'state': state,
                        'service': service_name
                    }
                    port_details.append(result)

                if mac_match:
                    result = {
                        'ip': current_ip,
                        'mac_address': mac_match.group(1),
                        'vendor': mac_match.group(2)
                    }
                    port_details.append(result)
                   
                if line == '\n':
                    results.append(port_details)
                    port_details = []
        
        return results


    def get_remote_device(self):
        # data ={
        #     "remote_ip_range" : facility_details['ip_address'],
        #     "password" : facility_details['password']
        # }
        facility_details = {
            "user_name" : "emruser",
            "password" : "lin@1088",
            "ip_address" : "10.40.30.3"
        }
        # remote = RemoteOperations()
        # client = remote.connect(facility_details)
        # data ={
        #     "remote_ip_range" : '10.40.30.0/24',
        #     "password" : 'lin@1088'
        # }
        # devices = remote.scan_remote_network(data,client)
        # Example usage:
        devices = ['Starting Nmap 7.94 ( https://nmap.org ) at 2023-05-29 21:18 CAT\n', 'Nmap scan report for 10.40.30.1\n', 'Host is up (0.00051s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', '23/tcp open  telnet\n', 'MAC Address: C0:14:FE:68:D0:A4 (Cisco Systems)\n', '\n', 'Nmap scan report for 10.40.30.2\n', 'Host is up (0.0098s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '5432/tcp open  postgresql\n', 'MAC Address: 00:0C:29:2C:6E:3E (VMware)\n', '\n', 'Nmap scan report for 10.40.30.4\n', 'Host is up (0.00016s latency).\n', 'Not shown: 95 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '21/tcp   open  ftp\n', '22/tcp   open  ssh\n', '23/tcp   open  telnet\n', '80/tcp   open  http\n', '2000/tcp open  cisco-sccp\n', 'MAC Address: 64:D1:54:5F:33:50 (Routerboard.com)\n', '\n', 'Nmap scan report for 10.40.30.5\n', 'Host is up (0.0079s latency).\n', 'Not shown: 95 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '21/tcp   open  ftp\n', '22/tcp   open  ssh\n', '23/tcp   open  telnet\n', '80/tcp   open  http\n', '2000/tcp open  cisco-sccp\n', 'MAC Address: 64:D1:54:5F:33:5E (Routerboard.com)\n', '\n', 'Nmap scan report for 10.40.30.6\n', 'Host is up (0.0095s latency).\n', 'Not shown: 94 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '3000/tcp open  ppp\n', '3306/tcp open  mysql\n', '5000/tcp open  upnp\n', '8000/tcp open  http-alt\n', 'MAC Address: 00:0C:29:80:DC:FB (VMware)\n', '\n', 'Nmap scan report for 10.40.30.11\n', 'Host is up (0.0088s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '3306/tcp open  mysql\n', 'MAC Address: 00:0C:29:B8:05:8C (VMware)\n', '\n', 'Nmap scan report for 10.40.30.12\n', 'Host is up (0.0088s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', '80/tcp open  http\n', 'MAC Address: 00:0C:29:E3:00:3C (VMware)\n', '\n', 'Nmap scan report for 10.40.30.16\n', 'Host is up (0.012s latency).\n', 'Not shown: 87 filtered tcp ports (no-response), 8 filtered tcp ports (host-prohibited)\n', 'PORT     STATE  SERVICE\n', '22/tcp   open   ssh\n', '80/tcp   closed http\n', '443/tcp  closed https\n', '3306/tcp open   mysql\n', '5432/tcp closed postgresql\n', 'MAC Address: 00:0C:29:DC:04:A6 (VMware)\n', '\n', 'Nmap scan report for 10.40.30.63\n', 'Host is up (0.0088s latency).\n', 'Not shown: 99 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', 'MAC Address: 00:0C:29:CA:15:1D (VMware)\n', '\n', 'Nmap scan report for 10.40.30.106\n', 'Host is up (0.0098s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '8000/tcp open  http-alt\n', 'MAC Address: 00:0C:29:80:15:03 (VMware)\n', '\n', 'Nmap scan report for 10.40.30.251\n', 'Host is up (0.00014s latency).\n', 'Not shown: 96 filtered tcp ports (no-response)\n', 'PORT     STATE  SERVICE\n', '22/tcp   closed ssh\n', '80/tcp   open   http\n', '443/tcp  open   https\n', '8000/tcp open   http-alt\n', 'MAC Address: CC:96:E5:F3:8A:B2 (Dell)\n', '\n', 'Nmap scan report for 10.40.30.3\n', 'Host is up (0.0000080s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '3306/tcp open  mysql\n', '8080/tcp open  http-proxy\n', '\n', 'Nmap done: 256 IP addresses (12 hosts up) scanned in 29.94 seconds\n']
        filtered_results =self.parse_nmap_scan(devices)

        # Print the filtered results
        for result in filtered_results:
        #     print(f"IP: {result['ip']}")
        #     print(f"Port: {result['port']}")
        #     print(f"State: {result['state']}")
        #     print(f"Service: {result['service']}")
        #     if 'mac_address' in result:
        #         print(f"MAC Address: {result['mac_address']}")
            print(result)
     

