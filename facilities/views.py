from django.shortcuts import render
from facilities.models import Facility
# from encounters.views import RemoteEncounters
from facilities.serializer import FacilitySerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions

# Create your views here.
class FacilityList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT d.id as district_id,f.id as facility_id,* FROM vpn v 
        INNER JOIN facilities f on f.id = v.facility_id
        INNER JOIN district d on f.district_id = d.id
        INNER JOIN zone z on d.zone_id = z.id 
        WHERE date = '{}';'''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
    
# Create your views here.
class Facilities(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM facilities ;'''
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
    
class OneFacilityData(APIView):
    def get(self,request,facility_id,start_date,end_date):
        service = ApplicationService()
        query ='''SELECT d.id as district_id,*  FROM encounters e
                INNER JOIN vpn v ON e.encounter_date = v.date
                INNER JOIN facilities f on f.id = v.facility_id
                INNER JOIN district d on f.district_id = d.id
                INNER JOIN zone z on d.zone_id = z.id
                WHERE 
                encounter_date BETWEEN {} AND {}
                AND e.facility_id = {} AND v.facility_id = {}
                order by encounter_date;'''.format(start_date,end_date,facility_id,facility_id)
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
class FacilityCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = FacilitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

class FacilityDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_facility_by_pk(self,pk):
        try:
            return Facility.objects.get(pk=pk)
        except:
            return False
 
    def get(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        facility.delete()
        return Response(status.HTTP_200_OK)
    
class facilityStatus(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self,request):
        try:
            facility = Facility.objects.get(ip_address=request.data['ip_address'])
        except Facility.DoesNotExist:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        if(request.data['element'] == 'get_devices'):
            facility.get_device_status = request.data['status']
        if(request.data['element'] == 'vl'):
            facility.viral_load = request.data['status']
        if(request.data['element'] == 'close_mon'):
            facility.close_monitoring_status = request.data['status']
        facility.save()
        return Response({
            'success': 'Viral Load status updated successfully'
        }, status=status.HTTP_200_OK)
        

class RemoteFacility():
    def create_facility(self,facility_name,facility_details):
        try:
            facility_details['facility_name'] =facility_name
            print(facility_details)
            facility = FacilityCreate()
            return (facility.post(facility_details).data)['id']
        except:
            print("======== facility id not available at ("+ facility_name +") =============")
        
    def get_remote_facility_name(self,data,client,remote):
        facility_name_query = '''"SELECT name as facility_name FROM global_property gp
                        INNER JOIN location l on gp.property_value = l.location_id
                        where property ='current_health_center_id';"'''
        return remote.execute_query(data, client, facility_name_query)

    def get_remote_dde(self,data,client,remote):
        dde_name_query = '''"SELECT property_value FROM global_property where property = 'dde_enabled';"'''
        dde_name = remote.execute_query(data, client, dde_name_query)
        if(len(dde_name)>1):
            return dde_name[1].rstrip('\n')
        else:
            return ''
    
    def save_dde(self,facility_id,data,client,remote):
        facility = Facility.objects.get(id=facility_id)
        facility.dde_enabled = self.get_remote_dde(data,client,remote)
        facility.save()

    def check_facility_existence(self,facility_name,facility_details):
        if facility_name:
            facility_name = facility_name[1].rstrip('\n')
            try:
                exisiting_facility = Facility.objects.get(facility_name=facility_name)
            except Facility.DoesNotExist:
                exisiting_facility =False
        else:
            return print(f"can not find remote facility = {facility_name}")

        if exisiting_facility:
            return exisiting_facility.id
        else:
            return self.create_facility(facility_name,facility_details)
    
    def process_facility_data(self,db_data,client,facility_details,remote):
        facility_name = self.get_remote_facility_name(db_data,client,remote)
        return self.check_facility_existence(facility_name,facility_details)