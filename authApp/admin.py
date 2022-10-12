from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models.clientes import Cliente
from .models.factura import Factura
from .models.operador import Operador
from .models.servicios import Servicio
from .models.mpago import Mpago

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

class ClienteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    readonly_fields = ("creacion", )
    search_fields = ['cedula','nombre']
    list_display = ('cedula','nombre','apellido','direccion','telefono','creacion')
    resource_class = ClienteResource

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura)
admin.site.register(Operador)
admin.site.register(Servicio)
admin.site.register(Mpago)

