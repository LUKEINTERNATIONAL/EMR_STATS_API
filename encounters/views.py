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
            "program_name" : result[1],
            "total_encounters" : result[2],
            "encounter_date" : datetime.today().strftime('%Y-%m-%d')
        }
        encounter = EcounterCreate()
        encounter.post(ecounter_data)

    def update_encounter(self,result):
        em = Enconters.objects.get(program_name=result[1], encounter_date = datetime.today().strftime('%Y-%m-%d'))
        em.total_encounters = result[2]
        em.save()

    def get_remote_encouters(self,facility_details,encounter_status):
        remote = remote_operations()
        client = remote.connect(facility_details['ip_address'],facility_details['user_name'],facility_details['password'])
        file = remote.open_remote_file(client, "/var/www/BHT-EMR-API/config/database.yml")
        try:
            data = yaml.safe_load(file)
            query = '''SELECT (SELECT property_value FROM openmrs_likuni.global_property 
                    where property ='current_health_center_name') as facility_name, 
                    p.name as program_name, count(*) as total_encounters FROM openmrs_likuni.encounter e 
                    INNER JOIN program p on p.program_id = e.program_id group by e.program_id;'''

            results = remote.connect_db(data['default']['username'],data['default']['password'],data['development']['database'],query)

            if(not Facility.objects.filter(facility_name=results[0][0]).exists()):
                facility_id = self.create_facilitly(results[0][0],facility_details)
            else:
                fm = Facility.objects.get(facility_name=results[0][0])
                facility_id = fm.id
       
            for result in results:
                if(encounter_status == 'create'):
                    self.create_encounter(facility_id,result)
                if(encounter_status == 'update'):
                    self.update_encounter(result)
        except yaml.YAMLError as exc:
            print(exc)

            
class SiteCreate(APIView):
    def post(self,request):
        remote = RemoteEncounters()
        return Response(remote.get_remote_encouters(request.data,'create'))

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

          



       

    


