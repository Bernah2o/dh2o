from multiprocessing.connection import Client
from django.db import models

from authApp.models.clientes import Cliente

class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, related_name='factura', on_delete=models.CASCADE)
    #operador = models.ForeignKey(Operador, related_name='operador', on_delete=models.CASCADE)
    #servicios = models.ForeignKey(Servicio, related_name='servicio', on_delete=models.CASCADE)
    fecha = models.DateField(max_length=50)
    cantidad_servicio = models.IntegerField()
    precio = models.IntegerField()
    modo_pago = models.CharField(max_length=50)
    tiempo_servicio = models.DateTimeField()
    descuento = models.IntegerField()