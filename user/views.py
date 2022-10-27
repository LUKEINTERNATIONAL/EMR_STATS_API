from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import logging

from user.serializer import LoginRequestSerializer, RegisterRequestSerializer

logging.basicConfig(level=logging.INFO)

class UserLogin(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = LoginRequestSerializer(data=data)
        if not serializer.is_valid():
            logging.warning(f"attempt login: Format Error")
            return Response({"status": "Fail to login"}, status=status.HTTP_401_UNAUTHORIZED)

        data = serializer.validated_data
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            logging.warning(f"attempt login: '{data['username']}' Authenticated FAILED")
            return Response({"status": "Fail to login"}, status=status.HTTP_401_UNAUTHORIZED)
        
        request.session["login"] = True
        request.session["username"] = data["username"]

        logging.info(f"login seccess: {data['username']}")
        return Response({"status": "OK"})

class UserTest(APIView):
    def get(self, request):
        if "login" in request.session:
            return Response({"logged in": request.session["login"], "username": request.session["username"]})
        else:
            return Response({"logged in": False, "username": None})

class UserRegister(APIView):
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = RegisterRequestSerializer(data=data)
        if not serializer.is_valid():
            logging.warning(f"attempt register: Format Error")
            return Response({"status": "Format Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        data = serializer.validated_data
        logging.info(data)
        try:
            user = User.objects.get(username=data["username"])
            logging.warning(f"attempt register: Username Existed")
            return Response({"status": "Username Existed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            pass
        
        if data["password"] != data["validate_password"]:
            logging.warning(f"attempt register: Password Validation Fail")
            return Response({"status": "Password Validation Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = User.objects.create_user(username=data["username"], password=data["password"], 
                                        email=data["email"] if "email" in data else None, 
                                        is_staff=False, is_superuser=False)
        user.save()
        
        return Response({"status": "OK"})

class UserLogout(APIView):
    def get(self,request):
        request.session["username"] = None
        request.session["login"] = False
        return Response({"status": "OK"})