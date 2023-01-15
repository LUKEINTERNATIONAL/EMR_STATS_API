import paramiko
import mysql.connector
import os
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
class remote_operations:
    def __init__(self):
        pass

    def connect(self, hostname, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, username=username, password=password,allow_agent=False)

            return client
        except Exception as e:
            return False
    
    def open_remote_file(self, ssh_client, filename):
        sftp_client = ssh_client.open_sftp()
        file = sftp_client.open(filename)
        return file

    def execute_query(self,user,passwd ,db, ssh_client, query):
        command = '''mysql -u{} -p{} {} -e {}'''.format(user,passwd,db,query)
        (stdin, stdout, stderr) = ssh_client.exec_command(command)
        print("The query was successful")
        return stdout.readlines()
    
    def ping(self,hostname):
        # hostname = "10.40.30.6" #example
        response = os.system("ping -c 1 " + hostname)
        #and then check the response...
        if response == 0:
          print(hostname, 'is up!')
          return True
        else:
          print(hostname, 'is down!')
          return False
    
    def ping_vpn(self):
         # hostname = "10.40.30.6" #example
        response = os.system("ping -c 1 " + config_data['vpn_ip'])
        #and then check the response...
        if response == 0:
          print(config_data['vpn_ip'], 'VPN is up!')
          return True
        else:
          print(config_data['vpn_ip'], 'VPN is down!')
          return False
