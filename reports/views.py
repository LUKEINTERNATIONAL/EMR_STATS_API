from django.shortcuts import render
from facilities.models import Facility
from rest_framework.views import APIView 
from users.custom_permissions import CustomPermissionMixin
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse

class UsabilityReportList(CustomPermissionMixin,APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM encounters e INNER JOIN facilities f on f.id = e.facility_id 
        WHERE encounter_date BETWEEN {} AND {}; '''.format(request.GET["start_date"],request.GET["end_date"])
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class TotalUsabilityReportList(CustomPermissionMixin,APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT facility_name,latitude,longitude ,vpn_status,encounter_date,
            SUM(total_patients) as total_patients, SUM(total_encounters) as total_encounters 
            FROM encounters e 
            INNER JOIN facilities f on f.id = e.facility_id 
            INNER JOIN vpn v on f.id = v.facility_id 
            WHERE encounter_date BETWEEN {} AND {}
            group by facility_name,latitude,longitude,vpn_status,encounter_date;
        '''.format(request.GET["start_date"],request.GET["end_date"])
        
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class FacilitiesWithCoordinates(CustomPermissionMixin,APIView):
   
    
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT 
                        facility_name,
                        latitude,
                        longitude ,
                        vpn_status,
                        encounter_date,
                        SUM(total_patients) as total_patients, 
                        SUM(total_encounters) as total_encounters 
            FROM facilities f 
            INNER JOIN encounters e on f.id = e.facility_id 
            INNER JOIN vpn v on f.id = v.facility_id 
            WHERE latitude !='' AND longitude !='' 
			AND date BETWEEN {} AND {} 
			AND encounter_date BETWEEN {} AND {}  
            group by 
			facility_name,
			latitude,
			longitude,vpn_status,encounter_date;
        '''.format(request.GET["start_date"],request.GET["end_date"],request.GET["start_date"],request.GET["end_date"])
        
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
  
        
class VPNReportList(CustomPermissionMixin,APIView):
   
    
    def get(self,request):
        service = ApplicationService()
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
                        where date BETWEEN {} AND {} {} group by 
                        {}
                    ) AS subquery;'''.format(columns,columns,request.GET["start_date"],request.GET["end_date"],where_facility,columns)

        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class ViralLoadList(CustomPermissionMixin,APIView):
   
    def get(self,request):
        service = ApplicationService()
        try:
            where_facility = '''AND v.facility_id={}'''.format(request.GET["facility_id"])
        except:
            where_facility = ''
        query ='''SELECT * FROM public.viral_load v
            INNER JOIN facilities f ON v.facility_id = f.id
           WHERE viral_load = '1' AND (DATE(v.created_at) BETWEEN {} AND {} OR (DATE(v.released_date) BETWEEN {} AND {} AND results IS NOT NULL)) 
           {}
           ;'''.format(request.GET["start_date"],request.GET["end_date"],request.GET["start_date"],request.GET["end_date"],where_facility)
        results = service.query_processor(query)
        return JsonResponse({
            'viral_load':results
        })