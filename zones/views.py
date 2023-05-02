from django.shortcuts import render
# from encounters.views import RemoteEncounters
from zones.serializer import ZoneSerializer
from zones.models import Zone
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions
# Create your views here.
class ZonesList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM zone'''
        results = service.query_processor(query)
        return JsonResponse({
            'zones':results
        })
    
class ZoneCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = ZoneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)    
        
class ZoneDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_zone_by_pk(self,pk):
        try:
            return Zone.objects.get(pk=pk)
        except:
            return False
 
    def get(self,request,pk):
        zone = self.get_zone_by_pk(pk)
        if zone == False:
            
            return Response({
                'error': 'Zone not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)

    def put(self,request,pk):
        zone = self.get_zone_by_pk(pk)
        if zone == False:
            return Response({
                'error': 'Zone not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ZoneSerializer(zone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        zone = self.get_zone_by_pk(pk)
        if zone == False:
            return Response({
                'error': 'Zone not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        zone.delete()
        return Response(status.HTTP_200_OK)
         