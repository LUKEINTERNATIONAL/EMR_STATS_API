import re
from services.remote_operations import RemoteOperations
from django.http import JsonResponse
from databases.serializer import DatabasesSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from databases.models import Databases
from django.db import connection
from service import ApplicationService
import os
import subprocess
from rest_framework import authentication, permissions
import logging
from facilities.models import Facility
from databases.tasks import copy_dumps_task
from django.forms.models import model_to_dict
import subprocess
from datetime import datetime
from sendfile import sendfile
from django.http import HttpResponse

logging.basicConfig(level=logging.INFO)

class DownloadDump(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,dump_name):
        # Construct the full file path
        file_path = os.path.expanduser("~")+'/Facilities_Backups/'+dump_name.replace("+", "/")
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        
class FacilityDumps(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def copy_dumps(self):
        facilities =Facility.objects.all()
        for facility in facilities:
            facility_data = {
                'facility_name':facility.facility_name,
                'password':facility.password,
                'user_name':facility.user_name,
                'ip_address':facility.ip_address
            }
            copy_dumps_task.delay(facility_data)
            
    def get_facility_dumps(self,path):
        try:
            command = "cd {} && ls -RAgo --si --time-style=long-iso {} ".format(path,"| awk '{print $3, $4, $5, $6}'")
            return subprocess.check_output(command, shell=True).decode('utf-8').split('\n')
        except:
            return ""
        
    def build_dump_progress(self):
        Databases.objects.all().delete()
        facilities =Facility.objects.all()
        for facility in facilities:
            facility_details = {
                'facility_name':facility.facility_name,
                'password':facility.password,
                'user_name':facility.user_name,
                'ip_address':facility.ip_address
            }
            remote = RemoteOperations()
            client = remote.connect(facility_details)
            command = '~/Facilities_Backups/{}/Backups'.format(facility_details["facility_name"])
            dumps = self.get_facility_dumps(command)
            for dump in dumps:
                dump_details =dump.split(' ')
                if(dump_details[0]):
                    dump_name = dump_details[3]
                    try:
                        remote_path = '/home/{}/backup/{}'.format(facility_details["user_name"],dump_name)
                        remote_size = remote.get_remote_file_size(client,remote_path)
                    except:
                        remote_path = '/home/{}/Backups/{}'.format(facility_details["user_name"],dump_name)
                        remote_size = remote.get_remote_file_size(client,remote_path)
                        
                    local_size = os.path.getsize(command+'/'+dump_name)
                    result = remote_size - local_size
                    percentage = (result / remote_size) * 100
                    
                    data = {
                            'facility_name': facility_details["facility_name"],
                            'dump_name': dump_name,
                            'progress':percentage
                        }
                    self.create_dump_details(data)
                    
    def create_dump_details(self,data):
        serializer = DatabasesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
                
        
        
    def get(self,request,facility_name):
        command = os.path.expanduser("~")+'/Facilities_Backups/{}/Backups'.format(facility_name)
        if os.path.exists(command) and os.path.isdir(command):
            pass
        else:
            command = os.path.expanduser("~")+'/Facilities_Backups/{}/backup'.format(facility_name)
        dumps = self.get_facility_dumps(command)
        dumps_filtered = []
        for dump in dumps:
            dump_details =dump.split(' ')
            #Databases.objects.get(facility_name = facility_name).progress
            if(dump_details[0]):
                dumps_details = {
                                    'dump_size':dump_details[0],
                                    'modified_date': dump_details[1]+" "+dump_details[2],
                                    'dump_name':dump_details[3],
                                    'progress':'',
                                    'dump_status':"",
                                }
                dumps_filtered.append(dumps_details)
        return JsonResponse({
         'facility_dumps':dumps_filtered
        }) 
    
    
class DumpsOverview(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def read_facilities_dump(self,path):
        command = "cd {} && du -x --si --time --max-depth=1".format(path)
        return subprocess.check_output(command, shell=True).decode('utf-8').split('\n')
         
    def get_size(self,path):
        command = 'du -sch '+path
        return subprocess.check_output(command, shell=True).decode('utf-8').split('\t')[0]
        
    def get_date_modified(self,path):
        mod_time = os.path.getmtime(path)
        return datetime.fromtimestamp(mod_time)
        
    def get(self,request):
        facilities = self.read_facilities_dump("~/Facilities_Backups")
        facilities_filter = []
        for facility in facilities:
            facility_details =facility.split('\t')
            if(len(facility_details) > 2):
                dumps_details = {
                                    'facility_name':facility_details[2].replace('./','').replace('.','_Total Size'),
                                    'total_dump_size':facility_details[0],
                                    'last_modified_date': facility_details[1],
                                    'overall_dump_status':"",
                                }
                facilities_filter.append(dumps_details)
           
        return JsonResponse({
            'facilities':facilities_filter
        }) 
                      