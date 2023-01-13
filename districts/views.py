from django.shortcuts import render
from districts.models import District
# from encounters.views import RemoteEncounters
from districts.serializer import DistrictSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions


# Create your views here.
class DistrictList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM district'''
        results = service.query_processor(query)
        return JsonResponse({
            'districts':results
        })
    
class DistrictCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = DistrictSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
            

class DistrictDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_facility_by_pk(self,pk):
        try:
            return District.objects.get(pk=pk)
        except:
            return False
 
    def get(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DistrictSerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        facility = self.get_facility_by_pk(pk)
        if facility == False:
            return Response({
                'error': 'Facility not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = DistrictSerializer(facility, data=request.data)
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
