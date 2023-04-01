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

logging.basicConfig(level=logging.INFO)

# Syncing of Database
           
# class DatabaseCreate(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self,request):
#         logging.warning(f"Posted data")
#         logging.warning(request.data)
#         serializer = DatabasesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
# class DatabaseList(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self,request):
#         service = ApplicationService()
#         query ='''SELECT * FROM databases; '''
#         results = service.query_processor(query)
#         return JsonResponse({
#             'databases':results
#         })

# class DatabaseDetails(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def process_all_databases(self):
#         database = Databases.objects.all()
#         for count,item in enumerate(database.values()):
#             remote = RemoteOperations()
#             if remote.ping(item["server_ip_address"]):
#                 process = subprocess.Popen(["pt-table-sync","--verbose","--database",item["database_name"],"--execute",\
#                                         "h={},u={},p={}".format(item["server_ip_address"],item["database_username"],item["database_password"]),\
#                                         "h=127.0.0.1,u=root,p=root","--noforeign-key-checks",\
#                                         "--nocheck-child-tables"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#                 result = process.communicate()
#                 for rs in result:
#                     print(rs)

# Syncing of Database end
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
    
    def get(self,request,facility_name):
        command = '~/Facilities_Backups/{}/Backups'.format(facility_name)
        dumps = self.get_facility_dumps(command)
        dumps_filtered = []
        for dump in dumps:
            dump_details =dump.split(' ')
            if(dump_details[0]):
                dumps_details = {
                                    'dump_size':dump_details[0],
                                    'modified_date': dump_details[1]+" "+dump_details[2],
                                    'dump_name':dump_details[3],
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
                      
            # os.system("sshpass -p 'lin@1088' rsync -vP emruser@10.40.30.6:~/euthini10102022_openmrs.sql .")
        # print(database.values_list())
        # for count,item in enumerate(database.values()):
        #     print(item)
            # command = '''pt-table-sync --verbose --databases {} --execute h={},u={},p={} h={},u={},p={} --noforeign-key-checks --nocheck-child-tables > /var/www/EMR_STATS_API/database_cronjob.log 2>&1'''\
            # .format(item["database_name"],item["server_ip_address"],item["database_username"],item["database_password"],'127.0.0.1','root','root')
        #     os.system(command)
                

    # def get_database_by_pk(self,pk):
    #     try:
    #         return  Databases.objects.get(pk=pk)
    #     except:
    #         return Response({
    #             'error': 'Book does not exist'
    #         }, status=status.HTTP_404_NOT_FOUND)
 
    # def get(self,request,pk):
    #     facility = self.get_facility_by_pk(pk)
    #     serializer = EncontersSerializer(facility)
    #     return Response(serializer.data)

    # def put(self,request,pk):
    #     facility = self.get_facility_by_pk(pk)
    #     serializer = EncontersSerializer(facility, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self,request,pk):
    #     facility = self.get_facility_by_pk(pk)
    #     facility.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)