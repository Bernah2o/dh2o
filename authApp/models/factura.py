<<<<<<< HEAD
from multiprocessing.connection import Client
from django.db import models

from authApp.models.clientes import Cliente
from authApp.models.operador import Operador
from authApp.models.servicios import Servicio

class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, related_name='factura', on_delete=models.CASCADE)
    operador = models.ForeignKey(Operador, related_name='operador', on_delete=models.CASCADE)
    servicios = models.ForeignKey(Servicio, related_name='servicio', on_delete=models.CASCADE)
    fecha = models.DateField(max_length=50)
    cantidad_servicio = models.IntegerField()
    precio = models.IntegerField()
    modo_pago = models.CharField(max_length=50)
    tiempo_servicio = models.DateTimeField()
    descuento = models.IntegerField()

    def __str__(self) -> str:
        return self.numero_factura
=======
from django.db import models

class Factura(models.Model):
    id = models.IntegerField(primary_key=True)
    cantidad = models.IntegerField()
    modo_pago = models.CharField(max_length=45)
    fecha = models.DateTimeField(max_length=100)
    
>>>>>>> 36107d8ab770179911347914ca535625d306f4d2
