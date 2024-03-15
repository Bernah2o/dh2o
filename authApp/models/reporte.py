from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
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
        if not self.pk:
            # Calcula la fecha de próxima limpieza sumando 6 meses a la fecha actual
            self.proxima_limpieza = self.fecha + relativedelta(months=6)

        # Marcar el servicio asociado como reportado al guardar el reporte
        if self.servicio_en_orden:
            self.servicio_en_orden.marcar_como_reportado()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Guardamos la orden de trabajo asociada antes de eliminar el reporte
        orden_de_trabajo = self.orden_de_trabajo

        # Eliminar el reporte
        super().delete(*args, **kwargs)

        # Verificar si la orden de trabajo aún tiene servicios sin reportar
        if orden_de_trabajo and not orden_de_trabajo.servicios_en_orden_detalle.filter(reportado=False).exists():
            # Actualizar el estado de reportado en la orden de trabajo si todos los servicios están reportados
            orden_de_trabajo.reportado = False
            orden_de_trabajo.save()

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


@receiver(post_delete, sender=Reporte)
def eliminar_reporte(sender, instance, **kwargs):
    # Cuando se elimina un reporte, actualizamos el estado de reportado en el servicio en orden
    if instance.servicio_en_orden:
        if instance.servicio_en_orden.reportado:
            # Si se elimina el reporte y el servicio en orden ya está reportado, lo marcamos como no reportado
            instance.servicio_en_orden.reportado = False
            instance.servicio_en_orden.save()
