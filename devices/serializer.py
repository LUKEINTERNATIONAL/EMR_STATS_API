from rest_framework import serializers
from devices.models import Device
from devices.models import DeviceServices

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class DeviceServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceServices
        fields = "__all__"