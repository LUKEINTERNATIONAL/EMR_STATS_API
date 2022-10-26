{
    "user_name" : "petros",
    "password" : "#p525263#",
    "ip_address" : "192.168.1.137"
}
{
    "user_name": "emruser",
    "password": "lin@1088",
    "ip_address": "192.168.11.190"
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