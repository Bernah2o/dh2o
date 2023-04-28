from django.db import models


class Servicio(models.Model):
    id_servicio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self) -> str:
        return self.nombre