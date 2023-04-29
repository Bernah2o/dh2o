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
    
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.direccion = self.direccion.upper()
        super(Cliente, self).save(*args, **kwargs)

    
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)

    

