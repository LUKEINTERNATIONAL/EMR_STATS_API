from encounters.views import EncouterDetails
from databases.views import DatabaseDetails
from databases.views import DatabaseDumps
from datetime import datetime
from sms.views import SMSDetails
from services.message_service import MessageService
from services.remote_operations import remote_operations



def my_scheduled_job():
    remote = remote_operations()
    if remote.ping_vpn():
        encounters = EncouterDetails()
        print("**************************************")
        print("Start processing data")
        print(datetime.now())
        print("**************************************")
        encounters.process_all_facilities()
        print("**************************************")
        print("End processing data")
        print(datetime.now())
        print("**************************************")
    else:
        print("==================== Can not update encounters VPN is Down==================")
        return False

def database_sync_job():
    # database = DatabaseDetails()
    # database.process_all_databases()
    remote = remote_operations()
    if remote.ping_vpn():
        databaseDumps = DatabaseDumps()
        databaseDumps.copy_dumps()
    else:
        print("==================== Can not copy dumps VPN is Down==================")
        return False

def send_messages():
    remote = remote_operations()
    if remote.ping_vpn():
        message = MessageService()
        message.send_messages()
    else:
        print("==================== Can not send Message VPN is Down==================")
        return False
    
