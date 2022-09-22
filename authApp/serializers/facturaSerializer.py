from authApp.models.factura import Factura
from rest_framework import serializers 

class facturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = [' numero_factura ','cliente','operador','servicios',
                    'fecha',' cantidad_servicio','precio','modo_pago','tiempo_servicio','descuento']