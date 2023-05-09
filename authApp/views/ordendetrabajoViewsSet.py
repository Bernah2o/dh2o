from rest_framework import viewsets
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.response import Response

from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item in data:
            if item['servicio']:
                item['precio'] = item['servicio']['precio']
        return Response(data)
    
@receiver(pre_save, sender=OrdenDeTrabajo)
def set_precio(sender, instance, **kwargs):
    servicio = instance.servicio
    if servicio:
        precio = servicio.precio
        instance.precio = precio    
