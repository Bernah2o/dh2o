from authApp.models.factura import Factura
from rest_framework import serializers 

class FacturaSerializer(serializers.ModelSerializer):
    servicios_realizados = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = '__all__'
        
    def get_servicios_realizados(self, obj):
        return obj.get_servicios_realizados()
