from django.db import models
from authApp.models.clientes import Cliente
from authApp.models.servicios import Servicio
from authApp.models.tanque import Tanque
from authApp.models.operador import Operador


class OrdenDeTrabajo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    descripcion = models.TextField()
    

    def __str__(self):
        return f"OrdenDeTrabajo {self.cliente}"
    
    
    