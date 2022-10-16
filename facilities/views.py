from django.shortcuts import render
from facilities.models import Facility
# from encounters.views import RemoteEncounters
from facilities.serializer import FacilitySerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class FacilityList(APIView):
    def get(self,request):
        facility = Facility.objects.all()
        serializer = FacilitySerializer(facility, many=True)
        return Response(serializer.data) 
    
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
            return Response({
                'error': 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
 
    def get(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
