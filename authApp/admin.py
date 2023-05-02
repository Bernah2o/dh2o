from datetime import date
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
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
        list_display = ('cedula','nombre','apellido','direccion','telefono','ver_clientes_proximos')
        list_display_links = ('cedula',)
        list_filter = ('creacion',)
        list_per_page = 10
        resource_class = ClienteResource
        
        def ver_clientes_proximos(self, obj):
            # Obtenemos la fecha actual y la última limpieza del cliente
            fecha_actual = date.today()
            ultima_limpieza = obj.ultima_limpieza
        
            # Si no hay fecha de última limpieza, devolvemos un mensaje indicando que no hay información
            if ultima_limpieza is None:
               return 'N/A'
        
            # Calculamos la cantidad de días desde la última limpieza
            dias_desde_limpieza = (fecha_actual - ultima_limpieza).days

            # Si la última limpieza fue hace más de 150 días, devolvemos un botón rojo
            if dias_desde_limpieza > 150:
                return mark_safe(f'<button class="boton-rojo">Prox. a vencerse</button>')
            # Si la última limpieza fue hace menos de 150 días, devolvemos un botón verde
            else:
                return mark_safe(f'<button class="boton-verde">Ok</button>')

        ver_clientes_proximos.short_description = 'Próx. a vencerse'
        ver_clientes_proximos.allow_tags = True
class Media:
        css = {
            'all': ('css/admin.css',)
        }      
    
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura)
admin.site.register(Operador)
admin.site.register(Servicio)
admin.site.register(Mpago)
admin.site.register(Tanque)
admin.site.register(Repuesto)
admin.site.register(OrdenDeTrabajo)
admin.site.register(Reporte)



