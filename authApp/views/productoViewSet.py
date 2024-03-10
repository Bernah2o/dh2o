from rest_framework import viewsets
from authApp.models.ordendetrabajo import ServicioEnOrden
from authApp.models.producto import Producto
from authApp.serializers.productoSerializer import ProductoSerializer
from django.shortcuts import render


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = []


def reporte_productos_view(request):
    productos = ServicioEnOrden.objects.select_related("orden", "orden__cliente").all()
    return render(request, "reporteproductos.html", {"productos": productos})
