from django.db import models
import locale
from collections import defaultdict
class OrdenDeTrabajo(models.Model):
    numero_orden = models.AutoField(primary_key=True)
    fecha = models.DateField()
    cliente = models.ForeignKey('authApp.Cliente', on_delete=models.CASCADE)
    servicios = models.ManyToManyField('authApp.Servicio')
    operador = models.ForeignKey('authApp.Operador', on_delete=models.CASCADE)
    descripcion = models.TextField()
    productos = models.ManyToManyField('authApp.Producto', blank=True)
    

    def __str__(self):
        return f"OrdenDeTrabajo {self.numero_orden}"
    
    def calcular_total(self):
        # Utilizar diccionarios para realizar el seguimiento de la cantidad y el precio de cada servicio y producto
        cantidad_servicios = {}
        precio_servicios = {}

        cantidad_productos = {}
        precio_productos = {}

        # Calcular la cantidad y el precio de cada servicio en la orden de trabajo
        for servicio in self.servicios.all():
            if servicio in cantidad_servicios:
                cantidad_servicios[servicio] += 1
            else:
                cantidad_servicios[servicio] = 1
                precio_servicios[servicio] = servicio.precio

        # Calcular la cantidad y el precio de cada producto en la orden de trabajo
        for producto in self.productos.all():
            if producto in cantidad_productos:
                cantidad_productos[producto] += 1
            else:
                cantidad_productos[producto] = 1
                precio_productos[producto] = producto.precio

        # Calcular el total sumando el precio de cada servicio y producto multiplicado por su cantidad
        total = 0

        for servicio, cantidad in cantidad_servicios.items():
            total += precio_servicios[servicio] * cantidad

        for producto, cantidad in cantidad_productos.items():
            total += precio_productos[producto] * cantidad

        return total