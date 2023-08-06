# Create your tasks here
import os
from celery import shared_task
from django.forms.models import model_to_dict

def make_dir(dirname):
    os.system("mkdir -p "+ dirname)

@shared_task(queue='copy_dumps')
def copy_dumps_task(facility):
    try:
        print("Start copying from "+facility['facility_name'])
        facility_name = facility['facility_name'].replace(' ', '_')
        make_dir("~/Facilities_Backups/"+facility_name)
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' {}@{}:~/Backups ~/Facilities_Backups/{}"
        .format(facility['password'],facility['user_name'],facility['ip_address'],facility_name))
        os.system("sshpass -p '{}' rsync -vP -r -e 'ssh -o StrictHostKeyChecking=no -p 22' {}@{}:~/backup ~/Facilities_Backups/{}"
        .format(facility['password'],facility['user_name'],facility['ip_address'],facility_name))
    except:
        print("Error can not copy from "+facility['facility_name'])