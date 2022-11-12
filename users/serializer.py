from pkg_resources import require
from rest_framework import serializers

class RegisterRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    validate_password = serializers.CharField(max_length=200)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

class PatchRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, required=False)
    validate_password = serializers.CharField(max_length=200, required=False)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)