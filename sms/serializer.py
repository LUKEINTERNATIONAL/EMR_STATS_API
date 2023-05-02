from rest_framework import serializers
from sms.models import SMS

class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = "__all__"
