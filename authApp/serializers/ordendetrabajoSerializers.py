from rest_framework import serializers
from django.db.models import Sum

from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.serializers.servicioSerializer import ServicioSerializer

class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True)
    precio = serializers.SerializerMethodField()
    
    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'

    def get_precio(self, obj):
        return obj.servicios.aggregate(total=Sum('precio'))['total']
 