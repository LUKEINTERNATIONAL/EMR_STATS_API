from django.shortcuts import render
from facilities.models import Facility
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions

# Create your views here.
class EncounterReportList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM encounters e INNER JOIN facilities f on f.id = e.facility_id 
        WHERE encounter_date BETWEEN {} AND {}; '''.format(request.GET["start_date"],request.GET["end_date"])
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
        
class VPNReportList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        # if "login" not in request.session:
        #     return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        # elif request.session["login"] == False:
        #     return Response({"status": "Denied"}, status=status.HTTP_401_UNAUTHORIZED)

        service = ApplicationService()
        query ='''SELECT * FROM vpn v INNER JOIN facilities f on f.id = v.facility_id 
        WHERE date BETWEEN {} AND {}; '''.format(request.GET["start_date"],request.GET["end_date"])
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })