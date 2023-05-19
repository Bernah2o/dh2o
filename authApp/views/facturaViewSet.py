from rest_framework import viewsets, permissions
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import action

from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import FacturaSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
            
    @action(detail=False, methods=['get'])
    def ventas_mensuales(self, request):
        ventas_mensuales = Factura.objects.annotate(mes=TruncMonth('creacion')).values('mes').annotate(total_ventas=Sum('total')).order_by('-mes')
        return Response(ventas_mensuales)
