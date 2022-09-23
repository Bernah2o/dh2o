from rest_framework import viewsets, permissions
from authApp.models.operador import Operador
from authApp.serializers.operadorSerializer import OperadorSerializer

class OperadorViewSet(viewsets.ModelViewSet):
    queryset = Operador.objects.all()
    serializer_class = OperadorSerializer
    permission_classes = [permissions.AllowAny]
