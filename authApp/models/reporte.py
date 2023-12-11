from dateutil.relativedelta import relativedelta
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
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

    def imprimir_pdf(self):
        url = reverse("admin:imprimir_pdf_reporte", args=[str(self.id_reporte)])
        return mark_safe(f'<a href="{url}" class="button">Imprimir PDF</a>')

    imprimir_pdf.short_description = "Imprimir PDF"

    def save(self, *args, **kwargs):
        # Calcula la fecha de próxima limpieza sumando 6 meses a la fecha actual
        if not self.proxima_limpieza:
            self.proxima_limpieza = self.fecha + relativedelta(months=6)
        super().save(*args, **kwargs)

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
