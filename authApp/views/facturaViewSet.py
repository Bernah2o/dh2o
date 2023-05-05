from rest_framework import viewsets, permissions
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.shortcuts import render
from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import FacturaSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.AllowAny]
    
def ventas_mensuales(request):
    ventas_mensuales = Factura.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total_ventas=Sum('total')).order_by('-mes')
    return render(request, 'ventas_mensuales.html', {'ventas_mensuales': ventas_mensuales})
