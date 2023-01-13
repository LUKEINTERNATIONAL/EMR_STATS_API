from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from rest_framework.views import APIView 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import logging
from service import ApplicationService
from django.http import JsonResponse
from users.models import CustomUser


from users.serializer import LoginRequestSerializer, RegisterRequestSerializer, PatchRequestSerializer
# from users.serializer import CustomUserSerializer

logging.basicConfig(level=logging.INFO)

# class UserLogin(APIView):
#     def post(self,request):
#         # try:
#         #     data = request.data  
#         # except AttributeError:
#         #     data = request
        
#         serializer = LoginRequestSerializer(data=data)
#         if not serializer.is_valid():
#             logging.warning(f"attempt login: Format Error")
#             return Response({"status": "Fail to login"}, status=status.HTTP_401_UNAUTHORIZED)

#         data = serializer.validated_data
#         user = authenticate(username=data["username"], password=data["password"])
#         if user is None:
#             logging.warning(f"attempt login: '{data['username']}' Authenticated FAILED")
#             return Response({"status": "Fail to login"}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request): # list user
        service = ApplicationService()
        query ='''SELECT * FROM users_customuser u INNER JOIN district d on d.id = u.district_id'''
        results = service.query_processor(query)
        return JsonResponse({
            'users':results
        })
        # users = get_user_model().objects.all()
        # result = []
        # for user in users:
        #     result.append({"username": user.username, "email": user.email, "is_staff": user.is_staff, 
        #                     "is_superuser": user.is_superuser})

        # return Response(result)
    
    def post(self, request): # register
      
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = RegisterRequestSerializer(data=data)
        if not serializer.is_valid():
            logging.warning(f"attempt register: Format Error")
            return Response({"status": "Format Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        data = serializer.validated_data
    
        try:
            user = CustomUser.objects.get(username=data["username"])
            logging.warning(f"attempt register: Username Existed")
            return Response({"status": "Username Existed"}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            pass
        
        if data["password"] != data["validate_password"]:
            logging.warning(f"attempt register: Password Validation Fail")
            return Response({"status": "Password Validation Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user = CustomUser(username=data["username"], 
                            password=data["password"], 
                            email=data["email"], 
                            is_superuser=data["is_superuser"],
                            district_id=data["district_id"],
                            name=data["name"],
                            phone=data["phone"],
                            )
        user.save()
        
        return Response({"status": "OK"})

class SingleUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            logging.warning(f"attempt get: Username Not Found")
            return Response({"status": "Username Not Found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"username": user.username, "email": user.email, "is_staff": user.is_staff, 
                            "is_superuser": user.is_superuser})

    def patch(self, request, username):
       
        try:
            data = request.data  
        except AttributeError:
            data = request
        
        serializer = PatchRequestSerializer(data=data)
        if not serializer.is_valid():
            logging.warning(f"attempt patch user: Format Error")
            return Response({"status": "Format Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if username != data["username"]:
            logging.warning(f"attempt patch user: Username Not Match {username} {data['username']}")
            return Response({"status": "Format Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        data = serializer.validated_data

      
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            logging.warning(f"attempt patch user: Username Not Found {username}")
            return Response({"status": "Username Not Found"}, status=status.HTTP_404_NOT_FOUND)
       
        if "password" in data and "validate_password" in data:
            if data["password"] != data["validate_password"]:
                logging.warning(f"attempt register: Password Validation Fail {username}")
                return Response({"status": "Password Validation Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user.set_password(data["password"])
        elif "password" not in data and "validate_password" not in data:
            pass
        else:
            logging.warning(f"attempt register: Password Validation Fail {username}")
            return Response({"status": "Password Validation Fail"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if "email" in data:
            user.email = data["email"]
        user.is_staff = data["is_staff"]
        user.is_superuser = data["is_superuser"]
        user.save()
        
        return Response({"status": "OK"})

    def delete(self, request, username):
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            logging.warning(f"attempt delete: Username Not Found")
            return Response({"status": "Username Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user.delete()
            return Response({"status": "OK"})
        except:
            logging.error(f"attempt delete {username}: server error")
            return Response({"status": "Username Not Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)