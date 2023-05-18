from rest_framework import viewsets, permissions
from authApp.models.servicios import Servicio
from authApp.serializers.servicioSerializer import ServicioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [permissions.IsAuthenticated]