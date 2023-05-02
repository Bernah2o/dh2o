from django.db import models
from django.core.validators import MinValueValidator

class Repuesto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del Repuesto')
    descripcion = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repuesto {self.nombre}"