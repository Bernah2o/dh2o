from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
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

    def generar_pdf(self, request, reporte_instance):
        cliente = reporte_instance.orden_de_trabajo.cliente
        servicio_en_orden = reporte_instance.servicio_en_orden

        # Ruta de la plantilla HTML
        template_path = "authApp/reporte_template.html"
        template = get_template(template_path)

        # Contexto para la plantilla
        context = {
            "reporte": reporte_instance,
            "imagen_antes_lavado_1": reporte_instance.imagen_antes_lavado_1.path,
            "imagen_antes_lavado_2": reporte_instance.imagen_antes_lavado_2.path,
            "imagen_despues_lavado_1": reporte_instance.imagen_despues_lavado_1.path,
            "imagen_despues_lavado_2": reporte_instance.imagen_despues_lavado_2.path,
        }

        # Renderizar la plantilla con el contexto
        html = template.render(context)

        try:
            # Crear el PDF usando xhtml2pdf
            pdf_response = HttpResponse(content_type="application/pdf")
            pdf_response["Content-Disposition"] = (
                f'filename="{reporte_instance.id_reporte}.pdf"'
            )
            pisa.CreatePDF(BytesIO(html), dest=pdf_response)
            return pdf_response

        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            raise RuntimeError(f"Error al generar el PDF: {e}")

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
                    servicio_en_orden=servicio_en_orden,  # Corregir aquí
                    fecha=timezone.now(),
                )
                reporte.save()
                reporte.generar_pdf()

    @property
    def cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    @staticmethod
    def buscar_por_cliente(cliente_id):
        return Reporte.objects.filter(orden_de_trabajo__cliente__id=cliente_id)
