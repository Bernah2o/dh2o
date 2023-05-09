from rest_framework import serializers
from authApp.models.ordendetrabajo import OrdenDeTrabajo

class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    precio = serializers.SerializerMethodField()

    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'

    def get_precio(self, obj):
        return obj.servicio.precio if obj.servicio else None