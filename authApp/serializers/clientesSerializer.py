from datetime import timedelta
from authApp.models.clientes import Cliente
from rest_framework import serializers 
from authApp.serializers.servicioSerializer import ServicioSerializer


class ClienteSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True, read_only=True)
    proxima_limpieza = serializers.DateField(read_only=True)
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'apellido', 'Fecha_nacimiento', 'direccion', 'telefono', 'correo', 'creacion', 'descripcion', 'ultima_limpieza', 'proxima_limpieza', 'servicios']
    
    def update(self, instance, validated_data):
        if 'ultima_limpieza' in validated_data:
            # Calcular fecha de próxima limpieza
            frecuencia_meses = 6 # Ejemplo, cambiar según necesidades
            delta_meses = timedelta(days=30*int(frecuencia_meses))
            instance.proxima_limpieza = validated_data['ultima_limpieza'] + delta_meses

        return super().update(instance, validated_data)    