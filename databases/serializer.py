from rest_framework import serializers
from databases.models import Databases

class DatabasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Databases
        fields = "__all__"
