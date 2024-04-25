from authApp.models.factura import Factura
from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from authApp.models.servicios import Servicio
from authApp.serializers.clientesSerializer import ClienteSerializer
from authApp.serializers.servicioSerializer import ServicioSerializer


class FacturaSerializer(serializers.ModelSerializer):
    creacion = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # servicios = serializers.PrimaryKeyRelatedField(
    #    many=True, queryset=Servicio.objects.all()
    # )
    servicios = ServicioSerializer(many=True, read_only=True)
    orden_de_trabajo = serializers.SerializerMethodField("get_orden_de_trabajo_details")
    cliente = ClienteSerializer(source="orden_de_trabajo.cliente", read_only=True)

    class Meta:
        model = Factura
        fields = "__all__"  # Incluye todos los campos del modelo, incluyendo 'creacion'

    def get_orden_de_trabajo_details(self, obj):
        return {
            "numero_orden": obj.orden_de_trabajo.numero_orden,
            "fecha": obj.orden_de_trabajo.fecha,
            "cliente": obj.orden_de_trabajo.cliente.nombre,
            # Otros campos de la orden de trabajo que desees incluir
        }

    def update(self, instance, validated_data):
        servicios_data = validated_data.pop("servicios", None)
        if servicios_data:
            instance.servicios.set(servicios_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
