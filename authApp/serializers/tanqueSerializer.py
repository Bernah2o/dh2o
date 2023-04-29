from rest_framework import serializers
from authApp.models.tanque import Tanque

class TanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tanque
        fields = '__all__'
