import paramiko
import mysql.connector

class remote_operations:
    def __init__(self):
        pass

    def connect(self, hostname, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, username=username, password=password)

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

    # def connect_db(self,user,passwd,db,hostname,query):
    #     config = {
    #         'user': user,
    #         'password': passwd,
    #         'host': hostname,
    #         'database': db,
    #         'raise_on_warnings': True
    #     }
    #     conn = mysql.connector.connect(**config)
    #     cur =conn.cursor()
    #     cur.execute(query)
    #     results = cur.fetchall()
    #     return results