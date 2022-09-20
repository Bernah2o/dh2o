from django.db import models

class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    documento = models.IntegerField()
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateTimeField(max_length=100)
    