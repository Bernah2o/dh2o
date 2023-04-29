from rest_framework import viewsets
from authApp.models.repuesto import Repuesto
from authApp.serializers.repuestoSerializers import RepuestoSerializer

class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer
