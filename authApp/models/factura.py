from django.db import models
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Sum
from authApp.models.clientes import Cliente

from authApp.models.mpago import Mpago
from authApp.models.ordendetrabajo import OrdenDeTrabajo



class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mpago = models.ForeignKey(Mpago, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True) 
           
    def __str__(self):
        return f"Factura {self.numero_factura} - Orden de Trabajo {self.orden_de_trabajo.numero_orden}"
    
    

        
        

        
    @staticmethod    
    def ventas_mensuales(request):
        ventas_mensuales = Factura.objects.annotate(mes=TruncMonth('creacion')).values('mes').annotate(total_ventas=Sum('total')).order_by('-mes')
        return render(request, 'ventas_mensuales.html', {'ventas_mensuales': ventas_mensuales})
    


