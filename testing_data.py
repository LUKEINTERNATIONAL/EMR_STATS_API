{
    "user_name" : "petros",
    "password" : "",
    "ip_address" : "192.168.1.137"
}
['Starting Nmap 7.94 ( https://nmap.org ) at 2023-05-29 21:18 CAT\n', 'Nmap scan report for 10.40.30.1\n', 'Host is up (0.00051s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', '23/tcp open  telnet\n', 'MAC Address: C0:14:FE:68:D0:A4 (Cisco Systems)\n', '\n', 'Nmap scan report for 10.40.30.2\n', 'Host is up (0.0098s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '5432/tcp open  postgresql\n', 'MAC Address: 00:0C:29:2C:6E:3E (VMware)\n', '\n', 'Nmap scan report for 10.40.30.4\n', 'Host is up (0.00016s latency).\n', 'Not shown: 95 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '21/tcp   open  ftp\n', '22/tcp   open  ssh\n', '23/tcp   open  telnet\n', '80/tcp   open  http\n', '2000/tcp open  cisco-sccp\n', 'MAC Address: 64:D1:54:5F:33:50 (Routerboard.com)\n', '\n', 'Nmap scan report for 10.40.30.5\n', 'Host is up (0.0079s latency).\n', 'Not shown: 95 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '21/tcp   open  ftp\n', '22/tcp   open  ssh\n', '23/tcp   open  telnet\n', '80/tcp   open  http\n', '2000/tcp open  cisco-sccp\n', 'MAC Address: 64:D1:54:5F:33:5E (Routerboard.com)\n', '\n', 'Nmap scan report for 10.40.30.6\n', 'Host is up (0.0095s latency).\n', 'Not shown: 94 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '3000/tcp open  ppp\n', '3306/tcp open  mysql\n', '5000/tcp open  upnp\n', '8000/tcp open  http-alt\n', 'MAC Address: 00:0C:29:80:DC:FB (VMware)\n', '\n', 'Nmap scan report for 10.40.30.11\n', 'Host is up (0.0088s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '3306/tcp open  mysql\n', 'MAC Address: 00:0C:29:B8:05:8C (VMware)\n', '\n', 'Nmap scan report for 10.40.30.12\n', 'Host is up (0.0088s latency).\n', 'Not shown: 98 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', '80/tcp open  http\n', 'MAC Address: 00:0C:29:E3:00:3C (VMware)\n', '\n', 'Nmap scan report for 10.40.30.16\n', 'Host is up (0.012s latency).\n', 'Not shown: 87 filtered tcp ports (no-response), 8 filtered tcp ports (host-prohibited)\n', 'PORT     STATE  SERVICE\n', '22/tcp   open   ssh\n', '80/tcp   closed http\n', '443/tcp  closed https\n', '3306/tcp open   mysql\n', '5432/tcp closed postgresql\n', 'MAC Address: 00:0C:29:DC:04:A6 (VMware)\n', '\n', 'Nmap scan report for 10.40.30.63\n', 'Host is up (0.0088s latency).\n', 'Not shown: 99 closed tcp ports (reset)\n', 'PORT   STATE SERVICE\n', '22/tcp open  ssh\n', 'MAC Address: 00:0C:29:CA:15:1D (VMware)\n', '\n', 'Nmap scan report for 10.40.30.106\n', 'Host is up (0.0098s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '80/tcp   open  http\n', '8000/tcp open  http-alt\n', 'MAC Address: 00:0C:29:80:15:03 (VMware)\n', '\n', 'Nmap scan report for 10.40.30.251\n', 'Host is up (0.00014s latency).\n', 'Not shown: 96 filtered tcp ports (no-response)\n', 'PORT     STATE  SERVICE\n', '22/tcp   closed ssh\n', '80/tcp   open   http\n', '443/tcp  open   https\n', '8000/tcp open   http-alt\n', 'MAC Address: CC:96:E5:F3:8A:B2 (Dell)\n', '\n', 'Nmap scan report for 10.40.30.3\n', 'Host is up (0.0000080s latency).\n', 'Not shown: 97 closed tcp ports (reset)\n', 'PORT     STATE SERVICE\n', '22/tcp   open  ssh\n', '3306/tcp open  mysql\n', '8080/tcp open  http-proxy\n', '\n', 'Nmap done: 256 IP addresses (12 hosts up) scanned in 29.94 seconds\n']
client = remote.connect("192.168.1.137","petros","")
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
    
     update 
  encounters 
set 
  total_encounters = 0,
  total_patients = 0
 where total_patients LIKE '2022-%'
 
 
 
 SELECT 
    e.encounter_id,
    e.patient_id,
    p.name AS program_name,
    et.name AS encounter_type,
    c.name AS value_coded
FROM encounter e
INNER JOIN program p ON p.program_id = e.program_id
INNER JOIN obs o ON o.encounter_id = e.encounter_id
INNER JOIN encounter_type et ON et.encounter_type_id = e.encounter_type
INNER JOIN concept_name c ON c.concept_id = o.value_coded
WHERE DATE(e.date_created) BETWEEN '2023-01-11' AND DATE(now())
GROUP BY e.encounter_id,e.patient_id,e.program_id,et.name,o.value_coded;