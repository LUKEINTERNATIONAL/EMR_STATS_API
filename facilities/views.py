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
        query ='''SELECT * FROM vpn v 
        INNER JOIN facilities f on f.id = v.facility_id
        INNER JOIN district d on f.district_id = d.id
        INNER JOIN zone z on d.zone_id = z.id 
        WHERE date = '{}';'''.format(datetime.today().strftime('%Y-%m-%d'))
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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
    def check_facility_existence(self,facility_name,facility_details):
        if facility_name:
            facility_name = facility_name[1].rstrip('\n')
            try:
                exisiting_facility = Facility.objects.get(facility_name=facility_name)
            except Facility.DoesNotExist:
                exisiting_facility =False
        else:
            return print("can not find remote facility")

        if exisiting_facility:
            return exisiting_facility.id
        elif "id" in facility_details:
            return self.create_facility(facility_name,facility_details)
    
    def process_facility_data(self,db_data,client,facility_details,remote):
        facility_name = self.get_remote_facility_name(db_data,client,remote)
        print(facility_name)
        return self.check_facility_existence(facility_name,facility_details)