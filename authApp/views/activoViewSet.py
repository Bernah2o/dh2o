from rest_framework import viewsets
from authApp.models.activo import Activo
from authApp.serializers.activoSerializer import ActivoSerializer

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.all()
    serializer_class = ActivoSerializer
    permission_classes = []

    