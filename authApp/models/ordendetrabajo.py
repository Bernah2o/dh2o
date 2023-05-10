from django.db import models
from authApp.models.clientes import Cliente
from authApp.models.servicios import Servicio
from authApp.models.tanque import Tanque
from authApp.models.operador import Operador


class OrdenDeTrabajo(models.Model):
    numero_orden = models.IntegerField(default=1, editable=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    descripcion = models.TextField()
    

    def __str__(self):
        return f"OrdenDeTrabajo {self.numero_orden} - {self.cliente}"

    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            # obtiene el último número de orden y suma 1
            ultimo_numero_orden = OrdenDeTrabajo.objects.all().order_by('-numero_orden').first()
            numero_orden = ultimo_numero_orden.numero_orden + 1 if ultimo_numero_orden else 1
            self.numero_orden = numero_orden
        super().save(*args, **kwargs)
        
    
    
    