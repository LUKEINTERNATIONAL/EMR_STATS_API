{
    "user_name" : "petros",
    "password" : "#p525263#",
    "ip_address" : "192.168.1.137"
}
facility_details ={
    "user_name": "linserver",
    "password": "lin1088",
    "ip_address": "10.40.30.3"
}
client = remote.connect("192.168.1.137","petros","#p525263#")
# SELECT DISTINCT(facility_id), MAX(encounter_date), f.password, f.user_name, f.ip_address FROM encounters e INNER JOIN facilities f on f.id = e.facility_id GROUP BY e.facility_id, f.password, f.user_name, f.ip_address

# def query_processor(self,query):
#         cursor = connection.cursor()
#         cursor.execute(query)
#         columns = [column[0] for column in cursor.description]
#         results = []
#         for row in cursor.fetchall():
#             results.append(dict(zip(columns, row)))
#         return results

cnx = mysql.connector.connect(user='root', password='root',
                              host='192.168.11.190',
                              database='openmrs_cb',
                              use_pure=False)

config = {
  'user': 'root',
  'password': 'root',
  'host': '192.168.11.190',
  'database': 'openmrs_cb',
  'raise_on_warnings': True
}
client = remote.connect('192.168.11.190','emruser','lin@1088')

process = subprocess.Popen(["pt-table-sync","--verbose","--databases","openmrs_likuni","--execute","h=10.40.30.6,u=root,p=root","h=127.0.0.1,u=root,p=root","--noforeign-key-che
     ...: cks","--nocheck-child-tables"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
     ...: result = process.communicate()
     ...: print(result)
     
    /usr/bin/python3 /var/www/EMR_STATS_API/manage.py crontab run 78c41cd35ad45af1d7b4300f7f73a619 >> /var/www/EMR_STATS_API/database_cronjob.log 2>&1