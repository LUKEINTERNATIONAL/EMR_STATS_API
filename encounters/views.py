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
from encounters.remote_encounters import RemoteEncounters
           
class SiteCreate(APIView):
    def post(self,request):
        remote = RemoteEncounters()
        return Response(remote.get_remote_encouters(request.data))

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
            "id" : facilities[count].facility.id, 
            "user_name" : facilities[count].facility.user_name,
            "password" : facilities[count].facility.password,
            "ip_address" : facilities[count].facility.ip_address
            }
            remote = RemoteEncounters()
            if(item['encounter_date'] == datetime.today().strftime('%Y-%m-%d')):
                print('updating encounter data')
                remote.get_remote_encouters(facility_data)
            else:
                print('create encounter data')
                remote.get_remote_encouters(facility_data)
                

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

          



       

    


