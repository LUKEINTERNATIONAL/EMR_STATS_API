from rest_framework import serializers
from viral_load.models import ViralLoad

class ViralLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViralLoad
        fields = "__all__"
