import csv
from encounters.remote_encounters import RemoteEncounters
with open('/var/www/facilities_ips.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        remote = RemoteEncounters()
        facility_details =[{
            "user_name": "linserver",
            "password": "lin1088",
            "ip_address": row[0]
        },
        {
            "user_name": "emruser",
            "password": "lin@1088",
            "ip_address": row[0]
        },
        {
            "user_name": "meduser",
            "password": "letmein",
            "ip_address": row[0]
        }]
        if(remote.get_remote_encouters(facility_details[0])):
            print("Successfully added 1")
        elif(remote.get_remote_encouters(facility_details[1])):
            print("Successfully added 2")
        elif(remote.get_remote_encouters(facility_details[2])):
            print("Successfully added 3")
