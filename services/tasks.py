# Create your tasks here
from services.remote_operations import RemoteOperations
import yaml
from facilities.views import RemoteFacility
from encounters.views import RemoteEncounters
from vpn.views import RemoteVNP
from viral_load.views import RemoteViralLoad
from devices.views import RemoteDevice
import os
import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
from celery import shared_task

@shared_task
def process_remote_data(facility_details):
    
    remote = RemoteOperations()
    response =remote.ping(facility_details['ip_address'])
    if(response):
        client = remote.connect(facility_details)
        if(client):
            try:
                db_data = remote.read_emr_db_file(client)
                if "id" in facility_details:
                    facility_id = facility_details["id"]
                else:
                    facility_id = RemoteFacility().process_facility_data(db_data,client,facility_details,remote)
                RemoteEncounters().process_encounter(db_data,client,facility_id,remote)
                bandwidth = RemoteVNP().getBandwidth(remote,client,facility_details['ip_address'])
                RemoteFacility().save_dde(facility_id,db_data,client,remote)
                RemoteVNP().process_vpn(facility_id,'active',response,bandwidth)
                if(facility_details['viral_load']=='1'):
                    RemoteViralLoad().process_lab_orders(db_data,client,facility_id,remote)
                if(facility_details['get_device_status']=='1'):
                    RemoteDevice().get_remote_device(client,facility_details,remote,facility_id)
            except yaml.YAMLError as exc:
                print(exc)
            client.close()
        else:
            print("Failed to login to  a remote server")
            return False
    elif "id" in facility_details:
        RemoteVNP().process_vpn(facility_details["id"],"inactive",response,[0,0])
        return False

@shared_task   
def send_sms_email(_url,data,message_type):
    try:
        requests.post(url = str(_url), json = data)
        print(f"Send {message_type} successful")
    
    except Exception as e:
        print(f"Failed to send {message_type}")
        print(f"Error: {e}")


