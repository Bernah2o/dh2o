from django.db import models
import locale
from authApp.models.clientes import Cliente
from authApp.models.producto import Producto
from authApp.models.servicios import Servicio
from authApp.models.operador import Operador


class OrdenDeTrabajo(models.Model):
    numero_orden = models.AutoField(primary_key=True)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    descripcion = models.TextField()
    productos = models.ManyToManyField(Producto, blank=True)
    

    def __str__(self):
        return f"OrdenDeTrabajo {self.numero_orden}"
    
    def calcular_total(self):
        total_servicios = sum(self.servicios.all().values_list('precio', flat=True))
        total_productos = sum(self.productos.all().values_list('precio', flat=True))
        total = total_servicios + total_productos
        # Configurar la configuración regional para Colombia
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

        # Formatear el total como pesos colombianos
        total_formateado = locale.currency(total, grouping=True, symbol=True)

        return total_formateado
    
    calcular_total.short_description = 'Total'
    
    
    
    