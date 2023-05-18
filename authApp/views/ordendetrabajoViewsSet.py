from rest_framework import viewsets, permissions

from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        servicios = self.request.data.pop('servicios', [])
        orden_de_trabajo = serializer.save()
        orden_de_trabajo.servicios.set(servicios)

    def perform_update(self, serializer):
        servicios = self.request.data.pop('servicios', [])
        orden_de_trabajo = serializer.save()
        orden_de_trabajo.servicios.set(servicios)
    
       
