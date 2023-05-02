from datetime import timezone
from django.shortcuts import render
from requests import request
from rest_framework import viewsets, permissions
from authApp.models.clientes import Cliente
from authApp.models.servicios import Servicio
from authApp.serializers.clientesSerializer import ClienteSerializer



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        servicios_data = self.request.data.get('servicios', [])
        cliente = serializer.save()

        for servicio_id in servicios_data:
            servicio = Servicio.objects.get(id=servicio_id)
            cliente.servicios.add(servicio)
            
    def clientes_proximos(self, request):
        clientes = Cliente.proximas_limpiezas()
        context = {'clientes': clientes}
        return render(request, 'authApp/clientes_proximos.html', context)
    def panel_clientes(request):
        clientes = ClienteViewSet.as_view({'get': 'clientes_proximos'})
        return clientes(request)
 
         
    
