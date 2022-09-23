from django.db import models

class Operario(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.IntegerField()
    telefono = models.IntegerField()
    email = models.EmailField(max_length=100)
    