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


# Create your views here.
class FacilityList(APIView):
    def get(self,request):
        if "login" not in request.session:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["login"] == False:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)

        service = ApplicationService()
        query ='''SELECT * FROM vpn v INNER JOIN facilities f on f.id = v.facility_id
         WHERE date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
    
class FacilityCreate(APIView):
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
    def get_facility_by_pk(self,pk):
        try:
            return Facility.objects.get(pk=pk)
        except:
            return False
 
    def get(self,request,pk):
        if "login" not in request.session:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["login"] == False:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        if "login" not in request.session:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["login"] == False:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["is_staff"] == False:
            return Response({"status": "You are not privileged"}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        if "login" not in request.session:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["login"] == False:
            return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.session["is_staff"] == False:
            return Response({"status": "You are not privileged"}, status=status.HTTP_401_UNAUTHORIZED)
        
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
