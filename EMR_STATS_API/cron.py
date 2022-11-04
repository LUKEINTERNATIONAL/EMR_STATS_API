from encounters.views import EncouterDetails
from datetime import datetime

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
