from django.db import models


class Mpago(models.Model):
    nombre = models.CharField(max_length=50)
    numero_cuenta = models.BigIntegerField()

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()  # Convierte el nombre a mayúsculas
        super(Mpago, self).save(*args, **kwargs)
