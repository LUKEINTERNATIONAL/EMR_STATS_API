from rest_framework import serializers
from zones.models import Zone

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"
