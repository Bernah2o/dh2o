from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from dateutil.relativedelta import relativedelta
from django.db import models
from authApp.models.ordendetrabajo import OrdenDeTrabajo


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
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

    def generar_pdf(request, reporte_id):
        reporte = get_object_or_404(Reporte, id_reporte=reporte_id)

        # Ruta de la plantilla HTML
        template_path = "authApp/reporte_template.html"
        template = get_template(template_path)

        # Contexto para la plantilla
        context = {
            "reporte": reporte,
            "imagen_antes_lavado_1": reporte.imagen_antes_lavado_1.path,
            "imagen_antes_lavado_2": reporte.imagen_antes_lavado_2.path,
            "imagen_despues_lavado_1": reporte.imagen_despues_lavado_1.path,
            "imagen_despues_lavado_2": reporte.imagen_despues_lavado_2.path,
        }

        # Renderizar la plantilla con el contexto
        html = template.render(context)

        try:
            # Crear el PDF usando xhtml2pdf
            pdf_response = HttpResponse(content_type="application/pdf")
            pdf_response["Content-Disposition"] = f'filename="{reporte.id_reporte}.pdf"'
            pisa.CreatePDF(BytesIO(html), dest=pdf_response)
            return pdf_response

        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            raise RuntimeError(f"Error al generar el PDF: {e}")

    def obtener_cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    obtener_cliente.short_description = "Cliente asociado"

    def total_servicio(self):
        return self.orden_de_trabajo.calcular_total()

    @property
    def cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    @staticmethod
    def buscar_por_cliente(cliente_id):
        return Reporte.objects.filter(orden_de_trabajo__cliente__id=cliente_id)
