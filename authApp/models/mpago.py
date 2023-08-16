from django.db import models


class Mpago(models.Model):
    id_mpago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()  # Convierte el nombre a mayúsculas
        super(Mpago, self).save(*args, **kwargs)
