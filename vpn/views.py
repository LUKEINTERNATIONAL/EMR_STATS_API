from django.shortcuts import render
from rest_framework.views import APIView 
from service import ApplicationService
from django.http import JsonResponse
from datetime import datetime
from vpn.models import VPN

from vpn.serializer import VPNSerializer
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService

# Create your views here.
class VPNCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = VPNSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VPNList(APIView):
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM vpn v INNER JOIN facilities f on f.id = v.facility_id 
        WHERE date = '{}'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'vpn':results
        })

class VPNDetail(APIView):
    def get_vpn_by_pk(self,pk):
        try:
            return VPN.objects.get(pk=pk)
        except:
            return Response({
                'error': 'Facility does not exit'
            }, status=status.HTTP_404_NOT_FOUND)
 
    def get(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        serializer = VPNSerializer(facility)
        return Response(serializer.data)

    def put(self,request,pk):
        vpn = self.get_vpn_by_pk(pk)
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = VPNSerializer(vpn, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        facility = self.get_vpn_by_pk(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)