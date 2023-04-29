from rest_framework import viewsets
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
