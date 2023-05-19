from authApp.models.factura import Factura
from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from authApp.models.servicios import Servicio 

class FacturaSerializer(serializers.ModelSerializer):
    creacion = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    
    class Meta:
        model = Factura
        fields = '__all__'  # Incluye todos los campos del modelo, incluyendo 'creacion'     
        
    def update(self, instance, validated_data):
        servicios_data = validated_data.pop('servicios', None)
        if servicios_data:
            instance.servicios.set(servicios_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance   
    
    
    
    
