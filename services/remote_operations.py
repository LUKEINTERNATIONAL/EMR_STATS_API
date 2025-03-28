import paramiko
import mysql.connector
import ping3
import os
import yaml
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
class RemoteOperations:
    def __init__(self):
        pass

    def connect(self, data):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=data['ip_address'], username=data['user_name'], password=data['password'],allow_agent=False)

            return client
        except Exception as e:
            return False
    
    def open_remote_file(self, ssh_client, filename):
        sftp_client = ssh_client.open_sftp()
        file = sftp_client.open(filename)
        return file
    
    def execute_command(self,command,ssh_client):
        (stdin, stdout, stderr) = ssh_client.exec_command(command)
        return stdout.readlines()

    def execute_query(self,data,ssh_client, query):
        command = '''mysql -u{} -p{} {} -e {}'''.format(data['username'],data['password'],data['database'],query)
        return self.execute_command(command,ssh_client)
    
    def scan_remote_network(self,data,ssh_client):
        command = '''echo {} | sudo -S nmap -p- -T4 {}'''.format(data['password'],data['remote_ip_range'])
        return self.execute_command(command,ssh_client)
    
    def scan_network_interface(self,ip_address,ssh_client):
        command = '''ip -o addr show | awk '/inet {}/ {{print $2}}' '''.format(ip_address)
        return self.execute_command(command,ssh_client)
    
    def scan_bandwidth(self,network_interface,ssh_client):
        command = '''cat /proc/net/dev | grep {} | awk -F':' '{{print $2}}' | awk '{{print $1, $9}}' '''.format(network_interface)
        return self.execute_command(command,ssh_client)
    
    def get_remote_file_size(self, ssh_client, remote_path):
        sftp_client = ssh_client.open_sftp()
        file2_size = sftp_client.stat(remote_path).st_size
        return file2_size
    
    # def ping(self,hostname):
    #     # hostname = "10.40.30.6" #example
    #     response = os.system("ping -c 1 " + hostname)
    #     #and then check the response...
    #     if response == 0:
    #       print(hostname, 'is up!')
    #       return True
    #     else:
    #         return False
        
    def ping(self,host):
        response = ping3.ping(host)
        if response is not None:
            return response
        else:
            return False
        
    def read_emr_db_file(self,client):
        try:
          file = self.open_remote_file(client, "/var/www/BHT-EMR-API/config/database.yml")
          data = yaml.safe_load(file)
          return {
              'username':data['default']['username'],
              'password':data['default']['password'],
              'database':data['development']['database'],
          }
        except IOError as e:
            print("Fail to find BHT-EMR-API database config")
            return False
   
