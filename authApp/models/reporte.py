from django.db import models
from authApp.models.ordendetrabajo import OrdenDeTrabajo

class Reporte(models.Model):
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='reportes/', blank=True, null=True)

    def __str__(self):
        return f"Reporte {self.orden_de_trabajo}"