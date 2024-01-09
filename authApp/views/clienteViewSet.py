from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import render
from authApp.models.clientes import Cliente
from authApp.serializers.clientesSerializer import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = []
        
    def clientes_proximos(self, request):
        clientes = Cliente.proximas_limpiezas()
        context = {"clientes": clientes}
        return render(request, "authApp/clientes_proximos.html", context)

    def panel_clientes(self, request):
        clientes = self.clientes_proximos(request)
        return clientes
