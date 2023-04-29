from rest_framework import serializers
from authApp.models.ordendetrabajo import OrdenDeTrabajo

class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'
