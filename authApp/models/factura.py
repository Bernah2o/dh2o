from django.db import models
from authApp.models.clientes import Cliente

from authApp.models.mpago import Mpago



class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey('authApp.OrdenDeTrabajo', on_delete=models.CASCADE, limit_choices_to={'factura__isnull': True})
    mpago = models.ForeignKey('authApp.Mpago', on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True) 
               
    @property
    def cliente(self):
        return self.orden_de_trabajo.cliente
    
    def __str__(self):
        return f"Factura {self.numero_factura}"
    
    def save(self, *args, **kwargs):
        self.total = self.orden_de_trabajo.calcular_total() - self.descuento
        super().save(*args, **kwargs)
        
   
    


