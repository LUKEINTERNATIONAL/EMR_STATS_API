from facilities.models import Facility
import os
from rest_framework.response import Response
from users.custom_permissions import CustomPermissionMixin
import os
import json
from pathlib import Path
from rest_framework.views import APIView 
from services.tasks import process_remote_data

BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))

class RemoteService(CustomPermissionMixin,APIView):
    
    def post(self,request):
        return Response(process_remote_data(request.data))
    
    def get_all_facility(self,type_data):
        facilities = Facility.objects.all()
        for count,item in enumerate(facilities.values()):
            facility_data = {
            "id" : facilities[count].id, 
            "user_name" : facilities[count].user_name,
            "password" : facilities[count].password,
            "ip_address" : facilities[count].ip_address,
            "district_id" : facilities[count].district_id,
            "get_device_status" : facilities[count].get_device_status,
            "viral_load" : facilities[count].viral_load,
            "type_data":type_data
            }
            process_remote_data.delay(facility_data)