from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.shortcuts import render
from rest_framework.response import Response

from authApp.models.clientes import Cliente
from authApp.serializers.clientesSerializer import ClienteSerializer
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
              
      
    def clientes_proximos(self, request):
        clientes = Cliente.proximas_limpiezas()
        context = {'clientes': clientes}
        return render(request, 'authApp/clientes_proximos.html', context)
    
    def panel_clientes(self, request):
        clientes = self.clientes_proximos(request)
        return clientes
    
    def enviar_whatsapp(self, request, cliente_id):
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        mensaje = 'Hola {} {}, este es un mensaje de prueba'.format(cliente.nombre, cliente.apellido)
        url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(cliente.telefono, mensaje)
        return HttpResponseRedirect(url)
    
