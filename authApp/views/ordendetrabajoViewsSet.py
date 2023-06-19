from rest_framework import viewsets
from decimal import Decimal
from django.shortcuts import render
from rest_framework.views import APIView



from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    permission_classes = [] # Permite el acceso sin autenticación
    
    def perform_create(self, serializer):
        servicios = self.request.data.pop('servicios', [])
        orden_de_trabajo = serializer.save()
        orden_de_trabajo.servicios.set(servicios)
        #orden_de_trabajo.calcular_comision()  # Calcular comisión al crear la orden de trabajo
    

    def perform_update(self, serializer):
        servicios = self.request.data.pop('servicios', [])
        orden_de_trabajo = serializer.save()
        orden_de_trabajo.servicios.set(servicios)
        #orden_de_trabajo.calcular_comision()  # Calcular comisión al actualizar la orden de trabajo
        
    

class CalcularComisionView(APIView):
    def get(self, request, pk):
        orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)
        comision = Decimal(0)
        for servicio in orden_de_trabajo.servicios.all():
            precio = servicio.precio
            comision += precio * Decimal('0.1')

        orden_de_trabajo.operador.comisiones += comision
        orden_de_trabajo.operador.save()

        # Convertir el objeto OrdenDeTrabajo a un diccionario
        orden_de_trabajo_dict = {
            'numero_orden': orden_de_trabajo.numero_orden,
            'operador': orden_de_trabajo.operador,
            'cliente': orden_de_trabajo.cliente,
            'fecha': orden_de_trabajo.fecha,
            # Agrega los campos adicionales que deseas incluir
        }

        context = {
            'orden_de_trabajo': orden_de_trabajo_dict,
            'comision': comision,
        }

        return render(request, 'calcular_comision.html', context)

