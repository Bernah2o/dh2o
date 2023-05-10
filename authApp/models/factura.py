from django.db import models

from authApp.models.mpago import Mpago
from authApp.models.clientes import Cliente


class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mpago = models.ForeignKey(Mpago, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True) 
       
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre} {self.cliente.apellido}"
    


