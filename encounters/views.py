import re
from remote_operations import remote_operations
from encounters.serializer import EncontersSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from datetime import datetime
import yaml
import requests
import json

data = json.load(open('config.json'))
base_url = data['base_url']
class RemoteEncounters:
    def create_facilitly(self,facility_name):
        facility_data = { 
            "facility_name" : facility_name,
            "user_name" : 'petros',
            "password" : '#p525263#',
            "ip_address" : '192.168.1.137'
        }
        r = requests.post(url = base_url+'facilities/', data = facility_data)
        return r.json()['id']
    def create_encounter(self,facility_id,result):
        ecounter_data = { 
            "facility_id" : facility_id,
            "program_name" : result[1],
            "total_encounters" : result[2],
            "encounter_date" : datetime.today().strftime('%Y-%m-%d')
        }
        requests.post(url = base_url+'encounters/', data = ecounter_data)
    def get_remote_encouters(self):
        remote = remote_operations()
        client = remote.connect('192.168.1.137','petros','#p525263#')
        file = remote.open_remote_file(client, "/var/www/BHT-EMR-API/config/database.yml")
        try:
            data = yaml.safe_load(file)
            query = '''SELECT (SELECT property_value FROM openmrs_likuni.global_property 
                    where property ='current_health_center_name') as facility_name, 
                    p.name as program_name, count(*) as total_encounters FROM openmrs_likuni.encounter e 
                    INNER JOIN program p on p.program_id = e.program_id group by e.program_id;'''

            results = remote.connect_db(data['default']['username'],data['default']['password'],data['development']['database'],query)
            print(results)
            facility_id = self.create_facilitly(results[0][0])

            for result in results:
                self.create_encounter(facility_id,result)
        except yaml.YAMLError as exc:
            print(exc)

class EcounterCreate(APIView):
    def post(self,request):
        serializer = EncontersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   

