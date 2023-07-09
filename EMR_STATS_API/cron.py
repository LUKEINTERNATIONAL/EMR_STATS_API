from services.remote_service import RemoteService
from databases.views import FacilityDumps
from datetime import datetime
from services.message_service import MessageService
from services.remote_operations import RemoteOperations
import os
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))

remote = RemoteOperations()
def my_scheduled_job():
    if remote.ping(config_data['vpn_ip']):
        remote_facility= RemoteService()
        remote_facility.get_all_facility('remote_data')
    else:
        return False

def get_all_devices():
    if remote.ping(config_data['vpn_ip']):
        remote_facility= RemoteService()
        remote_facility.get_all_facility('remote_devices')
    else:
        return False

def database_sync_job():
    # database = DatabaseDetails()
    # database.process_all_databases()
    if remote.ping(config_data['vpn_ip']):
        databaseDumps = FacilityDumps()
        databaseDumps.copy_dumps()
    else:
        print("==================== Can not copy dumps VPN is Down==================")
        return False

def send_messages():
    if remote.ping(config_data['vpn_ip']):
        message = MessageService()
        message.send_messages()
    else:
        print("==================== Can not send Message VPN is Down==================")
        return False
    
