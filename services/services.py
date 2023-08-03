from datetime import datetime,timedelta
import pytz
import os
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
config_data = json.load(open(os.path.join(BASE_DIR,'config.json')))
timezone = pytz.timezone('Africa/Blantyre')

def current_user_where(request):
    where_clause = ''
    if(request.user.zone_id is not 0):
        where_clause = ''' AND d.zone_id = {}'''.format(request.user.zone_id)
    elif(request.user.district_id is not 0):
        where_clause = ''' AND f.district_id = {}'''.format(request.user.district_id)
    return where_clause

def get_new_start_datetime(start_time_str,end_time_str):
    print('start_time_str****************')
    print(start_time_str)
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    seconds = (end_time - start_time).total_seconds()
    duration_hours = seconds // 3600
    duration_minutes = (seconds % 3600) // 60
    duration = timedelta(hours=duration_hours, minutes=duration_minutes)
    current_time = datetime.now(timezone)
    end_time = current_time - duration
    return end_time.strftime('%Y-%m-%d %H:%M:%S')

def get_time_different_in_minutes(date_str1,date_str2):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    date_obj1 = datetime.strptime(date_str1, datetime_format)
    date_obj2 = datetime.strptime(date_str2, datetime_format)
    time_difference = date_obj2 - date_obj1
    return time_difference.total_seconds() / 60