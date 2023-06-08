from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from authApp.models.producto import Producto
from authApp.serializers.productoSerializer import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
