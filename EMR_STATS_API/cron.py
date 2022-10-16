from encounters.views import EncouterDetails
def my_scheduled_job():
    encounters = EncouterDetails()
    print("**************************************")
    print("Start processing data")
    print("**************************************")
    encounters.process_all_facilities()
    print("**************************************")
    print("End processing data")
    print("**************************************")
