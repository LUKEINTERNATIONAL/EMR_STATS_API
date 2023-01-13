from rest_framework import serializers
from vpn_temp.models import VPNTemp

class VPNTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPNTemp
        fields = "__all__"
