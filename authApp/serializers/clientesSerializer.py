from authApp.models.clientes import Cliente
from rest_framework import serializers 

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['cedula','nombre','apellido','Fecha_nacimiento','direccion','telefono','correo']
        