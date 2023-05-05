from datetime import date
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils.html import format_html


# Importamos los modelos que queremos registrar
from .models.clientes import Cliente
from .models.factura import Factura
from .models.operador import Operador
from .models.servicios import Servicio
from .models.mpago import Mpago
from .models.tanque import Tanque
from .models.repuesto import Repuesto
from .models.ordendetrabajo import OrdenDeTrabajo
from .models.reporte import Reporte


# Definimos una clase que hereda de `resources.ModelResource` para especificar la configuración de importación/exportación
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

    # Definimos una clase que hereda de `ImportExportModelAdmin` y `admin.ModelAdmin` para personalizar el comportamiento del modelo en el sitio de administración


class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # Definimos que el campo `creacion` sea de solo lectura
    readonly_fields = ("creacion", )
    # Especificamos los campos por los que se puede realizar una búsqueda
    search_fields = ['cedula', 'nombre']
    # Especificamos los campos que se mostrarán en la lista de objetos del modelo
    list_display = ('cedula', 'nombre', 'apellido', 'direccion',
                    'telefono', 'ver_clientes_proximos')
    
    # Especificamos los campos que tendrán un enlace en la lista de objetos del modelo
    list_display_links = ('cedula', 'ver_clientes_proximos')
    # Especificamos los campos por los que se puede filtrar en la lista de objetos del modelo
    list_filter = ('creacion',)
    # Especificamos la cantidad de objetos que se mostrarán por página en la lista de objetos del modelo
    list_per_page = 10
    # Especificamos la configuración de importación/exportación del modelo
    resource_class = ClienteResource

    # Especificamos la hoja de estilos personalizada que queremos utilizar en la página de administración del modelo
    class Media:
        css = {
            'all': ('css/admin.css',)
        }
    
    
    # Definimos una función que nos permitirá mostrar un botón verde o rojo dependiendo de si el cliente está próximo a vencerse o no

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
            return mark_safe(f'<button class="boton-verde">Vigente</button>')
    
    def ver_clientes_proximos_column_header(self):
        return 'Estado'    

    ver_clientes_proximos.short_description = 'Estado'
    ver_clientes_proximos.allow_tags = True
    
    


class ReporteAdmin(admin.ModelAdmin):
    # Agregar una columna para el botón de descarga de PDF
    list_display = ['orden_de_trabajo', 'fecha', 'descripcion', 'ver_pdf']

    def ver_pdf(self, obj):
        # Generar la URL para descargar el PDF del reporte
        url = reverse('generar_reporte_pdf', args=[obj.id])

        # Retornar un enlace HTML con el botón de descarga del PDF
        return format_html('<a class="button" href="{}">PDF</a>', url)

    # Cambiar el título de la columna en la página de admin
    ver_pdf.short_description = 'Descargar'

class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'operador', 'mpago', 'fecha', 'descuento', 'total', 'ver_ventas_mensuales']
    list_display_links = ['numero_factura']
    # Otras configuraciones...

    def ver_ventas_mensuales(self, obj):
        url = reverse('ventas_mensuales')
        return format_html(f'<a href="{url}">Ver ventas mensuales</a>')

    ver_ventas_mensuales.short_description = 'Ventas mensuales'
    #numero_factura.short_description = 'No'

   


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Operador)
admin.site.register(Servicio)
admin.site.register(Mpago)
admin.site.register(Tanque)
admin.site.register(Repuesto)
admin.site.register(OrdenDeTrabajo)
admin.site.register(Reporte, ReporteAdmin)

