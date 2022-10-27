from rest_framework import serializers

class RegisterRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    validate_password = serializers.CharField(max_length=200)

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)