from rest_framework import serializers
from trackusers.models import TrackUsers

class TrackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackUsers
        fields = "__all__"
