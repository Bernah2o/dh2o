from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = (
            self.nombre.upper()
        )  # Convertir el nombre a mayúsculas antes de guardar
        super().save(
            *args, **kwargs
        )  # Llamar al método save de la clase padre para guardar los datos
