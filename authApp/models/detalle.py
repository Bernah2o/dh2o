from django.db import models

class Detalle(models.Model):
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    