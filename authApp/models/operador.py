from django.db import models

class Operador(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.IntegerField()
    
    def __str__(self) -> str:
        return self.nombre
