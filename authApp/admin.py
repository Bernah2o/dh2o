
from django.contrib import admin
# Register your models here.
from .models.clientes import Cliente
from .models.factura import Factura
from .models.operador import Operador
from .models.servicios import Servicio

admin.site.register(Cliente)
admin.site.register(Factura)
admin.site.register(Operador)
admin.site.register(Servicio)
