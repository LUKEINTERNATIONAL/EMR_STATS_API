# Create your tasks here
import os
from celery import shared_task
from django.forms.models import model_to_dict
import subprocess

def make_dir(dirname):
    os.system("mkdir -p "+ dirname)

@shared_task(queue='copy_dumps')
def copy_dumps_task(facility):
    copy_emr_dumps(facility)
    if not facility['ip_address_iblis']:
        pass
    else:
        copy_iblis_dumps(facility)
 
def copy_emr_dumps(facility):
    try:
        print("Start copying from "+facility['facility_name'])
        facility_name = facility['facility_name'].replace(' ', '_')
        make_dir("~/Facilities_Backups/"+facility_name)
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' {}@{}:~/remote_backups ~/Facilities_Backups/{}"
        .format(facility['password'],facility['user_name'],facility['ip_address'],facility_name))
    except:
        print("Error can not copy emr dump from "+facility['facility_name'])
         
def copy_iblis_dumps(facility):
    try:
        print("Start copying from "+facility['facility_name'])
        facility_name = facility['facility_name'].replace(' ', '_')
        make_dir("~/Facilities_Backups/"+facility_name)
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' {}@{}:~/remote_backups ~/Facilities_Backups/{}"
        .format(facility['password_iblis'],facility['user_name_iblis'],facility['ip_address_iblis'],facility_name))
    except:
        print("Error can not copy iblis dump from "+facility['facility_name'])
 
        
@shared_task(queue='create_dump')        
def create_dump_task(facility):
    create_emr_dumps(facility)
    if not facility['ip_address_iblis']:
        pass
    else:
        create_iblis_dumps(facility)
        
def create_emr_dumps(facility): 
    try:
        facility_name = facility['facility_name'].replace(' ', '_')
        make_dir("~/Facilities_Backups/"+facility_name)
        
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' ~/emr_remote_auto_database_backup.sh {}@{}:~/ "
        .format(facility['password'],facility['user_name'],facility['ip_address']))
        
        ssh_command = "sshpass -p {} ssh {}@{} 'bash -s' < {}  >> ~/Facilities_Backups/all_dumps.log 2>&1 &".format(facility['password'],facility['user_name'],facility['ip_address'],'/var/www/EMR_STATS_API/bin/emr_remote_auto_database_backup.sh')
        subprocess.run(ssh_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except:
        print("Error can not create emr backup for "+facility['facility_name']) 
         
def create_iblis_dumps(facility): 
    try:
        facility_name = facility['facility_name'].replace(' ', '_')
        make_dir("~/Facilities_Backups/"+facility_name)
        
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' ~/iblis_remote_auto_database_backup.sh {}@{}:~/ "
        .format(facility['password_iblis'],facility['user_name_iblis'],facility['ip_address_iblis']))
        
        ssh_command = "sshpass -p {} ssh {}@{} 'bash -s' < {}  >> ~/Facilities_Backups/all_dumps.log 2>&1 &".format(facility['password_iblis'],facility['user_name_iblis'],facility['ip_address_iblis'],'/var/www/EMR_STATS_API/bin/iblis_remote_auto_database_backup.sh')
        subprocess.run(ssh_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except:
        print("Error can not create iblis backup for "+facility['facility_name'])   
