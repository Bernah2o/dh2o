from rest_framework import viewsets
from decimal import Decimal
from django.shortcuts import render
from rest_framework.views import APIView
from authApp.models.clientes import Cliente
from authApp.models.ordendetrabajo import OrdenDeTrabajo, ServicioEnOrden
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer
from dal import autocomplete


class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    permission_classes = []  # Permite el acceso sin autenticación

    class ClienteAutoComplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            qs = Cliente.objects.all()

            if self.q:
                qs = qs.filter(nombre__icontains=self.q)

            return qs

    autocomplete_fields = {
        "cliente": ("authApp.Cliente", ClienteAutoComplete),
    }

    def perform_create(self, serializer):
        servicios_ids = self.request.data.pop("servicios", [])  # Obtener IDs de servicios
        orden_de_trabajo = serializer.save()

        # Crear instancias de ServicioEnOrden con los IDs proporcionados y la cantidad deseada
        nuevos_servicios_en_orden = [
            ServicioEnOrden(orden=orden_de_trabajo, servicio_id=servicio_id, cantidad=1)
            for servicio_id in servicios_ids
        ]
        ServicioEnOrden.objects.bulk_create(nuevos_servicios_en_orden)

        # Calcular el total después de guardar los cambios en la base de datos
        orden_de_trabajo.calcular_total()

    def perform_update(self, serializer):
        servicios_ids = self.request.data.pop("servicios", [])  # Obtener IDs de servicios
        orden_de_trabajo = serializer.save()

        # Limpiar los servicios existentes
        orden_de_trabajo.servicios_en_orden.clear()

        # Crear instancias de ServicioEnOrden con los IDs proporcionados y la cantidad deseada
        nuevos_servicios_en_orden = [
            ServicioEnOrden(orden=orden_de_trabajo, servicio_id=servicio_id, cantidad=1)
            for servicio_id in servicios_ids
        ]
        ServicioEnOrden.objects.bulk_create(nuevos_servicios_en_orden)

        # Calcular el total después de guardar los cambios en la base de datos
        orden_de_trabajo.calcular_total()

class CalcularComisionView(APIView):
    template_name = "calcular_comision.html"

    def get(self, request, pk):
        try:
            orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

            # Obtener la suma total de los precios de los servicios
            total_servicios = sum(
                servicio.precio for servicio in orden_de_trabajo.servicios.all()
            )

            # Calcular la comisión como el 10% de la suma total de servicios
            comision = total_servicios * Decimal("0.1")

            # Si la comisión es mayor que cero, agregarla al operador y guardar
            if comision > 0:
                orden_de_trabajo.operador.comisiones += comision
                orden_de_trabajo.operador.save()

            context = {
                "orden_de_trabajo": orden_de_trabajo,
                "comision": comision,
            }

            return render(request, self.template_name, context)
        except OrdenDeTrabajo.DoesNotExist:
            # Manejo de error si la orden de trabajo no existe
            return render(request, "orden_no_encontrada.html")
        except Exception as e:
            # Manejo de errores generales
            print("Error al calcular la comisión:", e)
            return render(request, "error_calculando_comision.html")
