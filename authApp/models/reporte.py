from django.db import models
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from django.urls import reverse
from django.utils.safestring import mark_safe




class Reporte(models.Model):
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='reportes/', blank=True, null=True)
    

    def imprimir_pdf(self):
        url = reverse('admin:imprimir_pdf_reporte', args=[str(self.id)])
        return mark_safe(f'<a href="{url}" class="button">Imprimir PDF</a>')

    imprimir_pdf.short_description = 'Imprimir PDF'
    
    def __str__(self):
        return f"Reporte {self.orden_de_trabajo}"