from django.db import models


class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True,)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField(max_length=50, blank=True)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=100, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True)
        
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)

    