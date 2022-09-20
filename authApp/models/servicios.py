from django.db import models

class Servicios(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200)
    precio = models.IntegerField()