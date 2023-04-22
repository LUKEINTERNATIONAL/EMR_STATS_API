from rest_framework import serializers
from vpn.models import VPN

class VPNSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPN
        fields = "__all__"
