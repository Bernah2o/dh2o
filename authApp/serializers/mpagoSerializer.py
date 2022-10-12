from authApp.models.mpago import Mpago
from rest_framework import serializers 

class MpagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mpago
        fields = ['nombre']