from django.db import models
from decimal import Decimal


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    ordenes_trabajo = models.ManyToManyField("authApp.OrdenDeTrabajo", blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = (
            self.nombre.upper()
        )  # Convertir el nombre a mayúsculas antes de guardar
        super(Producto, self).save(
            *args, **kwargs
        )  # Guardar el objeto en la base de datos
        
    def calcular_precio_con_incremento(self):
        incremento = self.precio * Decimal("0.30")  # Calcula el 30% del precio
        precio_con_incremento = self.precio + incremento
        return precio_con_incremento    
