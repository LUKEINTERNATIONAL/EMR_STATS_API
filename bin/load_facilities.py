import csv
from encounters.remote_encounters import RemoteEncounters
with open('/var/www/facilities_ips.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        remote = RemoteEncounters()
        facility_details =[{
            "user_name": "",
            "password": "",
            "ip_address": row[0]
        },
        {
            "user_name": "",
            "password": "",
            "ip_address": row[0]
        },
        {
            "user_name": "",
            "password": "",
            "ip_address": row[0]
        }]
        if(remote.process_remote_data(facility_details[0])):
            print("Successfully added 1")
        elif(remote.process_remote_data(facility_details[1])):
            print("Successfully added 2")
        elif(remote.process_remote_data(facility_details[2])):
            print("Successfully added 3")
