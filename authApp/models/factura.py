from django.db import models
from authApp.models.clientes import Cliente

from authApp.models.mpago import Mpago



class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey('authApp.OrdenDeTrabajo', on_delete=models.CASCADE, limit_choices_to={'factura__isnull': True})
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mpago = models.ForeignKey(Mpago, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True) 
               
    def __str__(self):
        return f"Factura {self.numero_factura} - Orden de Trabajo {self.orden_de_trabajo.numero_orden}"
    
    def save(self, *args, **kwargs):
        self.total = self.orden_de_trabajo.calcular_total() - self.descuento
        super().save(*args, **kwargs)
        
        
    """def clean(self):
        super().clean()
        if self.pk is None:
            # Validar solo al crear una nueva instancia de Factura
            ultima_factura = Factura.objects.order_by('-numero_factura').first()
            if ultima_factura is not None:
                siguiente_numero = ultima_factura.numero_factura + 1
                if siguiente_numero != 1:
                    raise ValidationError('El número de factura no es consecutivo.')
            else:
                if self.numero_factura != 1:
                    raise ValidationError('El número de factura debe ser 1 para la primera factura.') """   
    
    


