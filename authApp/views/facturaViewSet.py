from rest_framework import viewsets, permissions
from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import FacturaSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.AllowAny]
