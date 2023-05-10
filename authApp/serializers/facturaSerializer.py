from authApp.models.factura import Factura
from rest_framework import serializers 

class FacturaSerializer(serializers.ModelSerializer):
    creacion = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)


    class Meta:
        model = Factura
        fields = ['numero_factura','cliente','operador','mpago','descuento','descripcion','total','creacion']        
   
