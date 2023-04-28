from authApp.models.servicios import Servicio
from rest_framework import serializers 

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id_servicio', 'nombre', 'precio']