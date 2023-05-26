from dateutil.relativedelta import relativedelta
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from authApp.models.factura import Factura
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authApp.models.clientes import Cliente
class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
   
    ACTIVIDADES_CHOICES = [
        ('Act1', 'Inspección y riesgos: Identificar peligros y riesgos en el área.'),
        ('Act2', 'Cierre de entrada y salida: Verificar cierre para evitar ingreso de agua.'),
        ('Act3', 'Equipos de protección personal (EPP): Asegurar EPP necesarios.'),
        ('Act4', 'Bombeo y aspirado: Retirar agua del tanque con equipo.'),
        ('Act5', 'Limpieza del fondo: Remover sedimentos y residuos del fondo.'),
        ('Act6', 'Limpieza a presión: Limpiar paredes y techos con alta presión.'),
        ('Act7', 'Aspirado de residuos: Retirar agua sucia y residuos del tanque.'),
        ('Act8', 'Inspección final: Verificar limpieza y preparación para desinfección.'),
        # Agrega aquí más opciones de actividades según tus necesidades
    ]
    actividades_desarrolladas = MultiSelectField(choices=ACTIVIDADES_CHOICES, max_length=50,max_choices=8, default = None)
    imagen_antes_lavado_1 = models.ImageField(upload_to='reportes/', null=True)
    imagen_antes_lavado_2 = models.ImageField(upload_to='reportes/', null=True)
    imagen_despues_lavado_1 = models.ImageField(upload_to='reportes/', null=True)
    imagen_despues_lavado_2 = models.ImageField(upload_to='reportes/', null=True)
    proxima_limpieza = models.DateField(blank=True, null=True) 
    creacion = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Reporte {self.orden_de_trabajo.numero_orden}"
    
        
    def imprimir_pdf(self):
        url = reverse('admin:imprimir_pdf_reporte', args=[str(self.id_reporte)])
        return mark_safe(f'<a href="{url}" class="button">Imprimir PDF</a>')

    imprimir_pdf.short_description = 'Imprimir PDF'
    
    def save(self, *args, **kwargs):
        # Calcula la fecha de próxima limpieza sumando 6 meses a la fecha actual
        if not self.proxima_limpieza:
            self.proxima_limpieza = self.fecha + relativedelta(months=6)
        super().save(*args, **kwargs)
    
