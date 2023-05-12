from rest_framework import viewsets, permissions
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F
from django.shortcuts import render
from rest_framework.response import Response

from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import FacturaSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.AllowAny]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
            
def ventas_mensuales(request):
    ventas_mensuales = Factura.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total_ventas=Sum('total')).order_by('-mes')
    return render(request, 'ventas_mensuales.html', {'ventas_mensuales': ventas_mensuales})

