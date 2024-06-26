from rest_framework import viewsets
from authApp.models.clientes import Cliente
from authApp.serializers.clientesSerializer import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = []

