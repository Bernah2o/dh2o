from http import client
from django.db import models


class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=100)
        
    def __str__(self) -> str:
        return self .nombre    

    