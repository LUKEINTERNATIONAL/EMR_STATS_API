from rest_framework import serializers
from encounters.models import Enconters

class EncontersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enconters
        fields = "__all__"
