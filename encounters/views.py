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
            print("############################")
            print(serializer.data)
            return Response(serializer.data)
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
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

    def get_remote_encouters(self,facility_details):
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
            facility_id = self.create_facilitly(results[0][0],facility_details)

            for result in results:
                self.create_encounter(facility_id,result)
        except yaml.YAMLError as exc:
            print(exc)

            
class SiteCreate(APIView):
    def post(self,request):
        remote = RemoteEncounters()
        return Response(remote.get_remote_encouters(request.data))

class EncouterDetails(APIView):
    def get_all_new():
        # facilities_data =Enconters.objects.select_related('facility').order_by('-encounter_date')
        # for facility_data in facilities_data:
        #     print(facility_data.facility.facility_name)
        #     print(facility_data.encounter_date)

        cursor = connection.cursor()
        cursor.execute('''SELECT count(*) FROM people_person''')
        row = cursor.fetchone()



