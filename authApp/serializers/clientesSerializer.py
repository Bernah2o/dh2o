from datetime import timedelta, datetime
from django.utils import timezone
from authApp.models.clientes import Cliente
from rest_framework import serializers 
from authApp.serializers.servicioSerializer import ServicioSerializer


class ClienteSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True, read_only=True)
    proxima_limpieza = serializers.DateField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__' 
   
    def update(self, instance, validated_data):
        ultima_limpieza = validated_data.get('ultima_limpieza')
        if ultima_limpieza:
            # Calcular fecha de próxima limpieza
            frecuencia_meses = 6 # Ejemplo, cambiar según necesidades
            delta_meses = timedelta(days=30*int(frecuencia_meses))
            instance.proxima_limpieza = ultima_limpieza + delta_meses

        return super().update(instance, validated_data)   
    def get_proxima_limpieza(self, obj):
        delta = obj.proxima_limpieza - timezone.now().date()
        if delta.days <= 0:
            # Si la fecha ya pasó, mostrar "Vencido"
            return "Vencido"
        elif delta.days <= 180:
            # Si faltan menos de 180 días, mostrar en color naranja
            return f"<span style='color: orange'>{obj.proxima_limpieza}</span>"
        else:
            return obj.proxima_limpieza