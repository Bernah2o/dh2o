from rest_framework import viewsets, permissions
from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import facturaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = facturaSerializer
    permission_classes = [permissions.AllowAny]
