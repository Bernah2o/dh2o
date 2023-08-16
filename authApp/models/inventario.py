from django.db import models

from authApp.models.producto import Producto


class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    # Otros campos relevantes para el inventario

    def actualizar_cantidad(self, cantidad):
        # Actualiza la cantidad en el inventario
        self.cantidad = cantidad
        self.save()

    def save(self, *args, **kwargs):
        self.producto = self.producto.upper()  # Convierte el nombre a mayúsculas
        super(Inventario, self).save(*args, **kwargs)
