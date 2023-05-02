from authApp.models.factura import Factura
from rest_framework import serializers 

class FacturaSerializer(serializers.ModelSerializer):
    servicios_realizados = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = '__all__'
        
   
