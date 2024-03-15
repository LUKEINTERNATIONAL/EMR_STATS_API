import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EMR_STATS_API.settings')

app = Celery('EMR_STATS_API')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define the queues
app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'copy_dumps': {
        'exchange': 'copy_dumps',
        'routing_key': 'copy_dumps',
    },
    'create_dump': {
        'exchange': 'create_dump',
        'routing_key': 'create_dump',
    },
    'send_message': {
        'exchange': 'send_message',
        'routing_key': 'send_message',
    },
    'get_devices': {
        'exchange': 'get_devices',
        'routing_key': 'get_devices',
    },
    'get_remote_data': {
        'exchange': 'get_remote_data',
        'routing_key': 'get_remote_data',
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
