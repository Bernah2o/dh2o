from django.db import models
from authApp.models.servicios import Servicio
from authApp.models.operador import Operador
from authApp.models.mpago import Mpago
from authApp.models.clientes import Cliente


class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    mpago = models.ForeignKey(Mpago, on_delete=models.CASCADE)
    fecha = models.DateField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre} {self.cliente.apellido}"
    


