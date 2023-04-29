from rest_framework import viewsets
from authApp.models.tanque import Tanque
from authApp.serializers.tanqueSerializer import TanqueSerializer

class TanqueViewSet(viewsets.ModelViewSet):
    queryset = Tanque.objects.all()
    serializer_class = TanqueSerializer
