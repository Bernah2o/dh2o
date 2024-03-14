from rest_framework import viewsets
from decimal import Decimal
from django.shortcuts import render
from authApp.models.clientes import Cliente
from authApp.models.ordendetrabajo import OrdenDeTrabajo, ServicioEnOrden
from authApp.serializers.ordendetrabajoSerializers import OrdenDeTrabajoSerializer
from dal import autocomplete


class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer
    permission_classes = []  # Permite el acceso sin autenticación

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden_de_trabajo = self.get_object()
        servicios_en_orden = orden_de_trabajo.servicioenorden_set.all()
        context["servicios_en_orden"] = servicios_en_orden
        return context

    class ClienteAutoComplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            qs = Cliente.objects.all()

            if self.q:
                qs = qs.filter(nombre__icontains=self.q)

            return qs

    autocomplete_fields = {
        "cliente": ("authApp.Cliente", ClienteAutoComplete),
    }

    def _crear_servicios_en_orden(self, orden_de_trabajo, servicios_ids):
        nuevos_servicios_en_orden = [
            ServicioEnOrden(orden=orden_de_trabajo, servicio_id=servicio_id, cantidad=1)
            for servicio_id in servicios_ids
        ]
        ServicioEnOrden.objects.bulk_create(nuevos_servicios_en_orden)

    def perform_create(self, serializer):
        servicios_ids = self.request.data.pop(
            "servicios", []
        )  # Obtener IDs de servicios
        orden_de_trabajo = serializer.save()
        self._crear_servicios_en_orden(orden_de_trabajo, servicios_ids)
        orden_de_trabajo.calcular_total()

    def perform_update(self, serializer):
        servicios_ids = self.request.data.pop(
            "servicios", []
        )  # Obtener IDs de servicios
        orden_de_trabajo = serializer.save()
        orden_de_trabajo.servicios_en_orden.clear()
        self._crear_servicios_en_orden(orden_de_trabajo, servicios_ids)
        orden_de_trabajo.calcular_total()

    @classmethod
    def calcular_comision_view(self, request, pk):
        try:
            orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)
            comision = orden_de_trabajo.calcular_comision()
            context = {
                "orden_de_trabajo": orden_de_trabajo,
                "comision": comision,
            }
            return render(request, "calcular_comision.html", context)
        except OrdenDeTrabajo.DoesNotExist:
            return render(request, "orden_no_encontrada.html")
        except Exception as e:
            return render(request, "error_calculando_comision.html")
