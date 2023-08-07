from django.shortcuts import render
from facilities.models import Facility
from rest_framework.views import APIView 
from users.custom_permissions import CustomPermissionMixin
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from services import services
from trackusers.models import TrackUsers

service=ApplicationService()
class UsabilityReportList(CustomPermissionMixin,APIView):
    def get(self,request):
        query ='''SELECT * FROM encounters e 
        INNER JOIN facilities f on f.id = e.facility_id 
        LEFT JOIN district d on f.district_id = d.id
        LEFT JOIN zone z on d.zone_id = z.id 
        WHERE encounter_date BETWEEN {} AND {} {}; 
        '''.format(request.GET["start_date"],request.GET["end_date"],services.current_user_where(request))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class TotalUsabilityReportList(CustomPermissionMixin,APIView):
    def get(self,request):
        query ='''SELECT facility_name,latitude,longitude ,vpn_status,encounter_date,
            SUM(total_patients) as total_patients, SUM(total_encounters) as total_encounters 
            FROM encounters e 
            INNER JOIN facilities f on f.id = e.facility_id 
            INNER JOIN vpn v on f.id = v.facility_id 
            LEFT JOIN district d on f.district_id = d.id
            LEFT JOIN zone z on d.zone_id = z.id 
            WHERE encounter_date BETWEEN {} AND {} {}
            group by facility_name,latitude,longitude,vpn_status,encounter_date;
        '''.format(request.GET["start_date"],request.GET["end_date"],services.current_user_where(request))
        
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class FacilitiesWithCoordinates(CustomPermissionMixin,APIView):    
    def get(self,request):
        query ='''SELECT 
                        facility_name,
                        latitude,
                        longitude ,
                        vpn_status,
                        encounter_date,
                        SUM(total_patients) as total_patients, 
                        SUM(total_encounters) as total_encounters 
            FROM facilities f 
            INNER JOIN vpn v on f.id = v.facility_id 
            LEFT JOIN encounters e on f.id = e.facility_id AND encounter_date BETWEEN {} AND {}
            LEFT JOIN district d on f.district_id = d.id
            LEFT JOIN zone z on d.zone_id = z.id 
            WHERE latitude !='' AND longitude !='' 
			AND date BETWEEN {} AND {} {}
            group by 
			facility_name,
			latitude,
			longitude,vpn_status,encounter_date;
        '''.format(request.GET["start_date"],request.GET["end_date"],request.GET["start_date"],request.GET["end_date"],services.current_user_where(request))
        
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
  
        
class VPNReportList(CustomPermissionMixin,APIView):
   
    
    def get(self,request):
        if request.GET["start_date"] == request.GET["end_date"]:
            columns = 'facility_name,ip_address,vpn_status,date,response_time,transmitted_bandwidth,received_bandwidth'
        else:
            columns = 'facility_name,ip_address'

        try:
            if request.GET["per_day"] == 'true':
                columns = 'facility_name,ip_address,vpn_status,date,response_time,transmitted_bandwidth,received_bandwidth'
        except:
            pass

        try:
            where_facility = '''AND v.facility_id={}'''.format(request.GET["facility_id"])
        except:
            where_facility = ''

        query = '''SELECT 
                    CONCAT(
                        FLOOR(CAST(total_seconds AS integer) / 3600), ' hours, ',
                        FLOOR((CAST(total_seconds AS integer) % 3600) / 60), ' minutes'
                    ) AS total_time,
                    {}
                    FROM (
                    SELECT 
                        SUM(EXTRACT(EPOCH FROM (end_down_time::timestamp - start_down_time::timestamp))) AS total_seconds,
                        {}
                    FROM vpn v
                        INNER JOIN facilities f on f.id = v.facility_id 
                        LEFT JOIN district d on f.district_id = d.id
                        LEFT JOIN zone z on d.zone_id = z.id 
                        where date BETWEEN {} AND {} {} {} group by 
                        {}
                    ) AS subquery;'''.format(columns,columns,request.GET["start_date"],request.GET["end_date"],where_facility,services.current_user_where(request),columns)

        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class ViralLoadList(CustomPermissionMixin,APIView):
   
    def get(self,request):
        try:
            where_facility = '''AND v.facility_id={}'''.format(request.GET["facility_id"])
        except:
            where_facility = ''
        query ='''SELECT * FROM public.viral_load v
            INNER JOIN facilities f ON v.facility_id = f.id
            LEFT JOIN district d on f.district_id = d.id
            LEFT JOIN zone z on d.zone_id = z.id 
           WHERE viral_load = '1' AND (DATE(v.created_at) BETWEEN {} AND {} OR (DATE(v.released_date) BETWEEN {} AND {} AND results IS NOT NULL)) 
           {} {}
           ;'''.format(request.GET["start_date"],request.GET["end_date"],request.GET["start_date"],request.GET["end_date"],where_facility,services.current_user_where(request))
        results = service.query_processor(query)
        return JsonResponse({
            'viral_load':results
        })
    
class TrackSystemUser(CustomPermissionMixin,APIView):
    def get(self,request):
        where_clause = ''
        if(request.user.zone_id is not 0):
            where_clause = ''' AND u.zone_id = {} OR u.zone_id = 0'''.format(request.user.zone_id)
        elif(request.user.district_id is not 0):
            where_clause = ''' AND u.id = {}'''.format(request.user.id)
        columns = 'user_id,name,district,last_login'

        query ='''
        SELECT 
                    CONCAT(
                        FLOOR(CAST(total_seconds AS integer) / 3600), ' hours, ',
                        FLOOR((CAST(total_seconds AS integer) % 3600) / 60), ' minutes'
                    ) AS total_time,
                    {}
                    FROM (
                    SELECT 
                        SUM(EXTRACT(EPOCH FROM (logout_time::timestamp - login_time::timestamp))) AS total_seconds,
                        {}
                    FROM track_users t
                    INNER JOIN users_customuser u ON u.id = t.user_id
                    LEFT JOIN district d on u.district_id = d.id
                    LEFT JOIN zone z on d.zone_id = z.id
                    WHERE DATE(t.created_at) BETWEEN {} AND {} {} group by 
                        {}
                    ) AS subquery;
        
        '''.format(columns,columns,request.GET["start_date"],request.GET["end_date"],where_clause,columns)
        results = service.query_processor(query)
        return JsonResponse({
            'track_user':results
        })
