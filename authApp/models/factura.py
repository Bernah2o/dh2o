from django.db import models
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

from authApp.models.mpago import Mpago
from authApp.models.clientes import Cliente
from authApp.models.producto import Producto

from authApp.models.servicios import Servicio


class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cliente_ultima_limpieza = models.DateField(default=timezone.now)
    mpago = models.ForeignKey(Mpago, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True) 
    servicios = models.ManyToManyField(Servicio, blank=True)
    productos = models.ManyToManyField(Producto, blank=True)
    
       
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre} {self.cliente.apellido} - ${self.total.quantize(Decimal('.01')):,.2f}"
    
    def save(self, *args, **kwargs):
        self.fecha_ultima_limpieza = self.cliente.ultima_limpieza
        

        # Sumar el precio de los servicios y productos
        total_servicios = sum([s.precio for s in self.servicios.all()])
        total_productos = sum([p.precio for p in self.productos.all()])
        
         # Calcular el total de la factura
        self.total = total_servicios + total_productos - self.descuento
        
        super(Factura, self).save(*args, **kwargs)
        
    def ventas_mensuales(request):
        ventas_mensuales = Factura.objects.annotate(mes=TruncMonth('creacion')).values('mes').annotate(total_ventas=Sum('total')).order_by('-mes')
        return render(request, 'ventas_mensuales.html', {'ventas_mensuales': ventas_mensuales})
    


