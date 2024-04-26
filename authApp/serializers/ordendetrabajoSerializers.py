from rest_framework import serializers
from django.db.models import Sum

from authApp.models.ordendetrabajo import OrdenDeTrabajo, ServicioEnOrden


class ServicioEnOrdenSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.StringRelatedField(source="servicio", read_only=True)
    producto_nombre = serializers.StringRelatedField(source="producto", read_only=True)

    class Meta:
        model = ServicioEnOrden
        fields = (
            "id_servicio_en_orden",
            "servicio_nombre",
            "cantidad_servicio",
            "producto_nombre",
            "cantidad_producto",
        )


class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    servicios_en_orden = ServicioEnOrdenSerializer(
        many=True, read_only=True, source="servicios_en_orden_detalle"
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrdenDeTrabajo
        fields = "__all__"

    def get_total(self, obj):
        servicios_en_orden = obj.servicios_en_orden_detalle.all()
        total_servicios = sum(
            servicio.calcular_total() for servicio in servicios_en_orden
        )
        return total_servicios
