from django.db import models

class Servicio(models.Model):
    numerodeservicio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.numerodeservicio