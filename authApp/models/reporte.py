from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import models
from authApp.models.ordendetrabajo import OrdenDeTrabajo, ServicioEnOrden


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    servicio_en_orden = models.ForeignKey(
        ServicioEnOrden,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reportes",
    )
    fecha = models.DateField()
    imagen_antes_lavado_1 = models.ImageField(upload_to="reportes/", null=True)
    imagen_antes_lavado_2 = models.ImageField(upload_to="reportes/", null=True)
    imagen_despues_lavado_1 = models.ImageField(upload_to="reportes/", null=True)
    imagen_despues_lavado_2 = models.ImageField(upload_to="reportes/", null=True)
    proxima_limpieza = models.DateField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.orden_de_trabajo.numero_orden}"

    def save(self, *args, **kwargs):
        # Calcula la fecha de próxima limpieza sumando 6 meses a la fecha actual
        if not self.proxima_limpieza:
            self.proxima_limpieza = self.fecha + relativedelta(months=6)
        super().save(*args, **kwargs)

    def generar_reporte_pdf(request, pk):
        # Obtener la instancia del reporte
        reporte_instance = get_object_or_404(Reporte, pk=pk)

        # Generar el PDF del reporte
        pdf = reporte_instance.generar_pdf(request)

        # Devolver el PDF como una respuesta HTTP
        return HttpResponse(pdf, content_type="application/pdf")

    def total_servicio(self):
        # Obtener la factura asociada a la OrdenDeTrabajo
        factura = self.orden_de_trabajo.factura_set.first()
        if factura:
            return factura.total
        else:
            return None  # O el valor que prefieras en caso de no haber factura

    def generar_reportes_por_cliente(cliente_id):
        # Obtener todas las órdenes de trabajo del cliente
        ordenes_de_trabajo = OrdenDeTrabajo.objects.filter(cliente_id=cliente_id)

        for orden_de_trabajo in ordenes_de_trabajo:
            # Obtener los servicios asociados a la orden de trabajo
            servicios_en_orden = orden_de_trabajo.servicios_en_orden_detalle.all()

            for servicio_en_orden in servicios_en_orden:
                # Generar un reporte para cada servicio
                reporte = Reporte(
                    orden_de_trabajo=orden_de_trabajo,
                    servicio_en_orden=servicio_en_orden,
                    fecha=timezone.now(),
                )
                reporte.save()

    @property
    def cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    @staticmethod
    def buscar_por_cliente(cliente_id):
        return Reporte.objects.filter(orden_de_trabajo__cliente__id=cliente_id)
