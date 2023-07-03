from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView 
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import logging
from service import ApplicationService
from django.http import JsonResponse
from users.models import CustomUser
from users.serializer import RegisterRequestSerializer, PatchRequestSerializer, LoginSerializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login

logging.basicConfig(level=logging.INFO)      

class LoginAPIView(APIView): 
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                user = CustomUser.objects.get(username=username)
                return Response({
                    "message": "success", 
                    "code": status.HTTP_201_CREATED, 
                    "name": user.name,
                    "is_superuser": user.is_superuser,
                    "username": user.username,
                    "Token": token.key
                    })
            return Response(
                {"message": "error", "code": status.HTTP_401_UNAUTHORIZED, "details": ["Invalid credentials"]})
            
class UserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request): # list user
        service = ApplicationService()
        query ='''SELECT u.id as userid,u.zone_id as is_zone,* FROM users_customuser u 
        LEFT JOIN district d on d.id = u.district_id
        LEFT JOIN zone z on z.id = d.zone_id
        '''
        results = service.query_processor(query)
        return JsonResponse({
            'users':results
        })
    
class HisOfficer(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): # list user
        service = ApplicationService()
        query ='''SELECT * FROM users_customuser u 
        LEFT JOIN facilities f on f.district_id = u.district_id
        WHERE f.id = {}
        '''.format(request.GET['facility_id'])
        results = service.query_processor(query)
        return JsonResponse({
            'users':results
        })
    
    def post(self, request): 
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
        CustomUser.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=data["email"], 
            is_superuser=data["is_superuser"],
            district_id=data["district_id"] if data["district_id"] else 0,
            zone_id= data["zone_id"] if data["zone_id"] else 0,
            name=data["name"],
            phone=data["phone"],
        )
        return Response({"status": "OK"})
    
    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"status": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user.username = request.data['username']
        user.email = request.data['email']
        user.name = request.data['name']
        user.phone = request.data['phone']
        user.is_superuser = request.data['is_superuser']
        user.district_id = request.data['district_id'] if request.data['district_id'] else 0
        user.zone_id = request.data['zone_id'] if request.data['zone_id'] else 0
        user.save()
        return Response({"status": "OK"})
    
    def delete(self, request, pk):
        
        try:
            user = CustomUser.objects.get(id=pk)
        except ObjectDoesNotExist:
            logging.warning(f"attempt delete: Username Not Found")
            return Response({"status": "Username Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user.delete()
            return Response({"status": "OK"})
        except:
            logging.error(f"attempt delete {pk}: server error")
            return Response({"status": "Username Not Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    