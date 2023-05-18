from rest_framework import viewsets, permissions
from authApp.models.actividades import Actividad
from authApp.serializers.actividadSerializer import ActividadSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [permissions.IsAuthenticated]
