from encounters.views import EncouterDetails
from databases.views import DatabaseDetails
from databases.views import DatabaseDumps
from datetime import datetime
from sms.views import SMSDetails
from services.message_service import MessageService

def my_scheduled_job():
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

def database_sync_job():
    # database = DatabaseDetails()
    # database.process_all_databases()
    databaseDumps = DatabaseDumps()
    databaseDumps.copy_dumps()

def send_messages():
    message = MessageService()
    message.send_messages()
    
