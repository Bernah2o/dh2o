from django.db import models

class Factura(models.Model):
    fecha = models.DateField(max_length=50)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    modo_pago = models.CharField(max_length=50)
    tiempo = models.DateTimeField()
    descuento = models.IntegerField()
    