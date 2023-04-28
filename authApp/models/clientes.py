from django.db import models
from datetime import date, timedelta

from authApp.models.servicios import Servicio

class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=11)
    correo = models.EmailField(max_length=100, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True)
    ultima_limpieza = models.DateField(null=True, blank=True)
    necesita_limpieza_proximamente = models.BooleanField(default=False)
    servicios = models.ManyToManyField(Servicio)
    
    

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)

    def necesita_limpieza(self):
        if not self.ultima_limpieza or (date.today() - self.ultima_limpieza).days >= 180:
            return True
        return False

    necesita_limpieza.boolean = True
    necesita_limpieza.short_description = 'Necesita limpieza próximamente?'


