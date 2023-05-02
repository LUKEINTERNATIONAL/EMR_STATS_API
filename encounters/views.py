import re
from django.http import JsonResponse
from encounters.serializer import EncontersSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from datetime import datetime
from encounters.models import Enconters
from django.db import connection
from service import ApplicationService
from rest_framework import authentication, permissions

class EncounterList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM encounters e INNER JOIN facilities f on f.id = e.facility_id 
        WHERE encounter_date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })

class EncouterDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def query_processor(self,query):
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results            

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
    
class EcounterCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = EncontersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

class RemoteEncounters:
    def create_encounter(self,ecounter_data):
        encounter = EcounterCreate()
        encounter.post(ecounter_data)

    def update_encounter(self,result,em):
        em.total_encounters = result[1]
        em.total_patients = result[2]
        em.save()
   
    def get_remote_encounter_data(self,data,client,remote):
        usability_query = '''"SELECT p.name as program_name, count(*) as total_encounters,
            count(distinct(patient_id)) as total_patients FROM encounter e 
            INNER JOIN program p on p.program_id = e.program_id 
            WHERE DATE(e.date_created) = '{}' 
            group by e.program_id;"'''.format(datetime.today().strftime('%Y-%m-%d'))
        print(usability_query)
        return remote.execute_query(data, client, usability_query)
        
    def process_encounter(self,db_data,client,facility_id,remote):
        encounter_results=self.get_remote_encounter_data(db_data,client,remote)
        if encounter_results:
            del encounter_results[0]
            for result in encounter_results:
                result = result.rstrip('\n').split('\t')
                try:
                    encounter_exist = Enconters.objects.get(program_name=result[0], encounter_date = datetime.today().strftime('%Y-%m-%d'),facility_id =facility_id)
                except Enconters.DoesNotExist:
                    encounter_exist =False

                if(encounter_exist):
                    self.update_encounter(result,encounter_exist)
                else:
                    encounter_data = { 
                        "facility" : facility_id,
                        "program_name" : result[0],
                        "total_encounters" : result[1],
                        "total_patients": result[2],
                        "encounter_date" : datetime.today().strftime('%Y-%m-%d')
                    }
                    self.create_encounter(encounter_data)
        else:
            print(f"Encounters not found encounter_results = {encounter_results} facility_id ={facility_id} db_data = {db_data} client= {client} remote= {remote} ")
