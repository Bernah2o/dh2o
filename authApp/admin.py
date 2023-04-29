from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models.clientes import Cliente
from .models.factura import Factura
from .models.operador import Operador
from .models.servicios import Servicio
from .models.mpago import Mpago
from .models.tanque import Tanque
from .models.repuesto import Repuesto
from .models.ordendetrabajo import OrdenDeTrabajo
from .models.reporte import Reporte

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

class ClienteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
        readonly_fields = ("creacion", )
        search_fields = ['cedula','nombre']
        list_display = ('cedula','nombre','apellido','direccion','telefono','creacion')
        list_display_links = ('cedula',)
        list_filter = ('creacion',)
        list_per_page = 10
        resource_class = ClienteResource



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura)
admin.site.register(Operador)
admin.site.register(Servicio)
admin.site.register(Mpago)
admin.site.register(Tanque)
admin.site.register(Repuesto)
admin.site.register(OrdenDeTrabajo)
admin.site.register(Reporte)


