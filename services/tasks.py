# Create your tasks here
from services.remote_operations import RemoteOperations
import yaml
from facilities.views import RemoteFacility
from encounters.views import RemoteEncounters
from vpn.views import RemoteVNP
from viral_load.views import RemoteViralLoad
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
from celery import shared_task

@shared_task
def process_remote_data(facility_details):
    remote = RemoteOperations()
    vpn_status= RemoteVNP()
    if(vpn_status.check_facility_vpn(facility_details['ip_address']) == "active"):
        client = remote.connect(facility_details)
        if(client):
            try:
                db_data = remote.read_emr_db_file(client)
                facility_id = RemoteFacility().process_facility_data(db_data,client,facility_details,remote)
                RemoteEncounters().process_encounter(db_data,client,facility_id,remote)
                RemoteVNP().process_vpn(facility_id,'active')
                RemoteViralLoad().process_lab_orders(db_data,client,facility_id,remote)
            except yaml.YAMLError as exc:
                print(exc)
        else:
            print("Failed to login to  a remote server")
            return False
    elif "id" in facility_details:
        RemoteVNP().process_vpn(facility_details["id"],"inactive")
        return False
