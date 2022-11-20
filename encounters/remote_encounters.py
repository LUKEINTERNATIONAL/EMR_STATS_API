import re

from remote_operations import remote_operations
from datetime import datetime
import yaml
from facilities.views import FacilityCreate
from facilities.models import Facility
from encounters.models import Enconters
from vpn.models import VPN
from vpn import views
import os
from encounters.create_encouter import EcounterCreate

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
            "total_patients": result[2],
            "encounter_date" : datetime.today().strftime('%Y-%m-%d')
        }
        encounter = EcounterCreate()
        encounter.post(ecounter_data)

    def update_encounter(self,result,em):
        em.total_encounters = result[1]
        em.total_patients = result[2]
        em.save()

    def vpn_processor(self,facility_id,status):
        try:
            vpn_results = VPN.objects.get(date=datetime.today().strftime('%Y-%m-%d'), facility_id=facility_id)
        except VPN.DoesNotExist:
            vpn_results = False
            print("VPN failed to update or create")

        vpn_data = {
            "facility": facility_id,
            "vpn_status" : status,
            "date"       : datetime.today().strftime('%Y-%m-%d')
        }

        if vpn_results:
            vpn =views.VPNDetail()
            vpn.put(vpn_data,vpn_results.id)
            print("vpn status updated")
        else:
            vpn = views.VPNCreate()
            vpn.post(vpn_data)
            print("vpn status created")
            
   
    def get_remote_encouters(self,facility_details):
        remote = remote_operations()
        if remote.ping(facility_details['ip_address']):
            client = remote.connect(facility_details['ip_address'],facility_details['user_name'],facility_details['password'])
            if(client):
                print("Client connection successful")
                file = remote.open_remote_file(client, "/var/www/BHT-EMR-API/config/database.yml")
                try:
                    data = yaml.safe_load(file)
                
                    facility_query = '''"SELECT property_value as facility_name FROM global_property where property =\'current_health_center_name\';"'''
                
                    encounter_query = '''"SELECT p.name as program_name, count(*) as total_encounters,
                    count(distinct(patient_id)) as total_patients FROM encounter e 
                    INNER JOIN program p on p.program_id = e.program_id 
                    WHERE DATE(e.date_created) = '{}' 
                    group by e.program_id;"'''.format(datetime.today().strftime('%Y-%m-%d'))

                    encounter_results = remote.execute_query(data['default']['username'],data['default']['password'] ,data['development']['database'], client, encounter_query)
                    facility_results = remote.execute_query(data['default']['username'],data['default']['password'] ,data['development']['database'], client, facility_query)
                    
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
                    
                    print("####### Start vpn #######")
                    self.vpn_processor(facility_id,"active")
                    

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
                                self.create_encounter(facility_id,result)
                    else:
                        print("Encounters not found")
                except yaml.YAMLError as exc:
                    print(exc)
            else:
                print("Failed to login to  a remote server")
        elif "id" in facility_details:
                self.vpn_processor(facility_details["id"],"inactive")
           





          



       

    


