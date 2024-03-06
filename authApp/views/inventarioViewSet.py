from authApp.models.inventario import Inventario
from authApp.serializers.inventarioSerializer import InventarioSerializer
from rest_framework import viewsets


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = []
