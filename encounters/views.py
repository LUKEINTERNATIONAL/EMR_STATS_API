import re

from django.http import JsonResponse
from remote_operations import remote_operations
from encounters.serializer import EncontersSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from datetime import datetime
import yaml
from facilities.views import FacilityCreate
from facilities.models import Facility
from encounters.models import Enconters
from django.db import connection
from service import ApplicationService
from rest_framework import serializers
import json
import logging
import os

class EcounterCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        print(data)
        serializer = EncontersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class RemoteEncounters:
    def create_facilitly(self,facility_name,facility_details):
        facility_data = { 
            "facility_name" : facility_name,
            "user_name" : facility_details['user_name'],
            "password" : facility_details['password'],
            "ip_address" : facility_details['ip_address']
        }
        facility = FacilityCreate()
        return (facility.post(facility_data).data)['id']

    def create_encounter(self,facility_id,result):
        ecounter_data = { 
            "facility" : facility_id,
            "program_name" : result[0],
            "total_encounters" : result[1],
            "encounter_date" : datetime.today().strftime('%Y-%m-%d')
        }
        encounter = EcounterCreate()
        encounter.post(ecounter_data)

    def update_encounter(self,result):
        em = Enconters.objects.get(program_name=result[0], encounter_date = datetime.today().strftime('%Y-%m-%d'))
        em.total_encounters = result[1]
        em.save()

    def get_remote_encouters(self,facility_details,encounter_status):
        remote = remote_operations()
        client = remote.connect(facility_details['ip_address'],facility_details['user_name'],facility_details['password'])
        if(client):
            file = remote.open_remote_file(client, "/var/www/BHT-EMR-API/config/database.yml")
            try:
                data = yaml.safe_load(file)
             
                facility_query = '''"SELECT property_value as facility_name FROM global_property where property =\'current_health_center_name\';"'''
               
                encounter_query = '''"SELECT p.name as program_name, count(*) as total_encounters FROM encounter e 
                        INNER JOIN program p on p.program_id = e.program_id WHERE DATE(e.date_created) = '{}' 
                        group by e.program_id;"'''.format(datetime.today().strftime('%Y-%m-%d'))

                encounter_results = remote.execute_query(data['default']['username'],data['default']['password'] ,data['development']['database'], client, encounter_query)
                facility_results = remote.execute_query(data['default']['username'],data['default']['password'] ,data['development']['database'], client, facility_query)

            
                print(encounter_results)
                print(facility_results)

                if facility_results:
                    facility_results = facility_results[1].rstrip('\n')
                    try:
                        exisiting_facility = Facility.objects.get(facility_name=facility_results)
                    except Facility.DoesNotExist:
                        exisiting_facility =False
                else:
                    return print("can not find remote facility")

                if exisiting_facility:
                    facility_id = exisiting_facility.id
                else:
                    facility_id = self.create_facilitly(facility_results,facility_details)

                if encounter_results:
                    del encounter_results[0]
                    for result in encounter_results:
                        result = result.rstrip('\n').split('\t')
                        print(result)
                        if(encounter_status == 'create'):
                            self.create_encounter(facility_id,result)
                        if(encounter_status == 'update'):
                            self.update_encounter(result)
                else:
                    print("Encounters not found")
            except yaml.YAMLError as exc:
                print(exc)
        else:
            print("fail to connect")

            
class SiteCreate(APIView):
    def post(self,request):
        remote = RemoteEncounters()
        return Response(remote.get_remote_encouters(request.data,'create'))

class EncounterList(APIView):
    def get(self,request):
        if "login" not in request.session:
            return Response({"status": "Denied"}, status=status.HTTP_403_FORBIDDEN)
        elif request.session["login"] == False:
            return Response({"status": "Denied"}, status=status.HTTP_403_FORBIDDEN)

        service = ApplicationService()
        query ='''SELECT * FROM encounters e INNER JOIN facilities f on f.id = e.facility_id 
        WHERE encounter_date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })

class EncouterDetails(APIView):
    def query_processor(self,query):
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def process_all_facilities(self):
        facilities =Enconters.objects.order_by('facility_id','-encounter_date').distinct('facility_id')
        print(facilities.values_list())
        for count,item in enumerate(facilities.values()):
            facility_data = { 
            "user_name" : facilities[count].facility.user_name,
            "password" : facilities[count].facility.password,
            "ip_address" : facilities[count].facility.ip_address
            }
            remote = RemoteEncounters()
            if(item['encounter_date'] == datetime.today().strftime('%Y-%m-%d')):
                remote.get_remote_encouters(facility_data,'update')
            else:
                remote.get_remote_encouters(facility_data,'create')
                

    def get_facility_by_pk(self,pk):
        try:
            return Enconters.objects.get(pk=pk)
        except:
            return Response({
                'error': 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
 
    def get(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        serializer = EncontersSerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        serializer = EncontersSerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

          



       

    


