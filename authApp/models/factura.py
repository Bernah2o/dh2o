from multiprocessing.connection import Client
from django.db import models

from authApp.models.clientes import Cliente
from authApp.models.mpago import Mpago
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
    mpago = models.ForeignKey(Mpago, related_name='mpago', on_delete=models.CASCADE)
    tiempo_servicio = models.DurationField()
    descuento = models.IntegerField(blank=True)
    total_servicio = models.IntegerField()

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)
    
    
    def suma_valores(self):
        return (self.precio * self.cantidad_servicio)
    
    def save(self):
        self.total_servicio = self.suma_valores
        super (Factura, self).save()
      
