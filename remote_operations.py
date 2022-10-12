import paramiko
import mysql.connector

class remote_operations:
    def __init__(self):
        pass

    def connect(self, hostname, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, username=username, password=password)
        return client
    
    def open_remote_file(self, ssh_client, filename):
        sftp_client = ssh_client.open_sftp()
        file = sftp_client.open(filename)
        return file

    def connect_db(self,user,passwd,db,query):
        conn = mysql.connector.connect(host='127.0.0.1',
                   user=user,
                   passwd=passwd,
                   port=3306,
                   db=db)
        cur =conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        return results