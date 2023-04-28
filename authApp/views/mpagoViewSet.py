from rest_framework import viewsets, permissions
from authApp.models.mpago import Mpago
from authApp.serializers.mpagoSerializer import MpagoSerializer

class MpagoViewSet(viewsets.ModelViewSet):
    queryset = Mpago.objects.all()
    serializer_class = MpagoSerializer
    permission_classes = [permissions.AllowAny]