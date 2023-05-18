from authApp.models.factura import Factura
from rest_framework import serializers
from authApp.models.servicios import Servicio 

class FacturaSerializer(serializers.ModelSerializer):
    creacion = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())
    

    class Meta:
        model = Factura
        fields = ['numero_factura','cliente','operador','mpago','descuento','descripcion','total','creacion']     
        
    def update(self, instance, validated_data):
        servicios_data = validated_data.pop('servicios', None)
        if servicios_data:
            instance.servicios.set(servicios_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance       
   
