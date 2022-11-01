import re

from encounters.serializer import EncontersSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 

class EcounterCreate(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = EncontersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



          



       

    


