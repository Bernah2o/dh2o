from django.db import models

class Repuesto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"Repuesto {self.nombre}"