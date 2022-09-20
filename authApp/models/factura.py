from django.db import models

class Factura(models.Model):
    id = models.IntegerField(primary_key=True)
    cantidad = models.IntegerField()
    modo_pago = models.CharField(max_length=45)
    fecha = models.DateTimeField(max_length=100)
    