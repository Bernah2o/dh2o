from datetime import date
from django.contrib import admin
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils.html import format_html
from django import forms
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import locale
from django.utils.timezone import localtime
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.admin.views.main import ChangeList



# Importamos los modelos que queremos registrar
from .models.clientes import Cliente
from .models.factura import Factura
from .models.operador import Operador
from .models.servicios import Servicio
from .models.mpago import Mpago
from .models.ordendetrabajo import OrdenDeTrabajo
from .models.reporte import Reporte
from .models.actividades import Actividad
from .models.producto import Producto
from decimal import Decimal
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
        
        # Si la última limpieza fue hace más de 180 días, devolvemos un botón naranja con el mensaje "Vencido"
        if dias_desde_limpieza > 180:
             return mark_safe(f'<button class="boton-naranja">Vencido</button>')
        # Si la última limpieza fue hace más de 150 días pero menos de 180 días, devolvemos un botón rojo
        elif dias_desde_limpieza > 150:
            return mark_safe(f'<button class="boton-rojo">Llamar</button>')
        # Si la última limpieza fue hace menos de 150 días, devolvemos un botón verde
        else:
            return mark_safe(f'<button class="boton-verde">Vigente</button>')
    
    def ver_clientes_proximos_column_header(self):
        return 'Estado'    

    ver_clientes_proximos.short_description = 'Estado'
    ver_clientes_proximos.allow_tags = True
    
      
class ReporteAdmin(admin.ModelAdmin):
    # Agregar una columna para el botón de descarga de PDF
    list_display = ['orden_de_trabajo','cliente','fecha','ver_pdf',]
    search_fields = ('cliente__nombre',)
    readonly_fields = ('creacion','proxima_limpieza',) # campo inmodificable
    
    
    def ver_pdf(self, obj):
        # Generar la URL para descargar el PDF del reporte
        url = reverse('generar_reporte_pdf', args=[obj.id_reporte])

        # Retornar un enlace HTML con el botón de descarga del PDF
        return format_html('<a class="button" href="{}">PDF</a>', url)

    # Cambiar el título de la columna en la página de admin
    ver_pdf.short_description = 'Descargar'
    
class FacturaAdmin(admin.ModelAdmin):
    readonly_fields = ('creacion',)  # Establece campos de solo lectura
    actions = ['ventas_mensuales_action']  # Agrega una acción personalizada
    list_display = ('numero_factura', 'cliente', 'formatted_total','ventas_mensuales_column')  # Campos a mostrar en la lista de objetos
    list_filter = (('creacion', admin.DateFieldListFilter),)  # Filtros por fecha de creación

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(mes=TruncMonth('creacion')).annotate(total_ventas=Sum('total')).order_by('-mes')
        return queryset
    
    def ventas_mensuales_column(self, obj):
        # Crear el enlace para redirigir a ventas_mensuales.html
        link = reverse('ventas_mensuales')
        link_html = format_html('<a href="{}" target="_blank">Ver Ventas Mensuales</a>', link)
        
        return link_html

    ventas_mensuales_column.short_description = 'Ventas Mensuales'
    
    def formatted_total(self, obj):
        total_formatted = f"{obj.total:,.2f}".rstrip('0').rstrip('.')
        return format_html(f"${total_formatted} COP")


    formatted_total.short_description = 'Total'

    def save_model(self, request, obj, form, change):
        # Verificar si es una nueva factura sin número asignado
        if not obj.numero_factura:
            # Obtener el último número de factura existente
            ultimo_numero_factura = Factura.objects.order_by('-numero_factura').first()

            # Establecer el nuevo número de factura
            if ultimo_numero_factura:
                obj.numero_factura = ultimo_numero_factura.numero_factura + 1
            else:
                obj.numero_factura = 1

        super().save_model(request, obj, form, change) 
    
class OrdenDeTrabajoForm(forms.ModelForm):
    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'

class OrdenDeTrabajoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'fecha', 'cliente', 'formatted_total','enlace_comisiones')
    form = OrdenDeTrabajoForm  
    
    def formatted_total(self, obj):
        total = obj.calcular_total()
        total_formatted = f"{total:,.2f}".rstrip('0').rstrip('.')
        return format_html(f"${total_formatted} COP")

    formatted_total.short_description = 'Total'
    
    def enlace_comisiones(self, obj):
        enlace = reverse('authApp_ordendetrabajo_comisiones', args=[obj.pk])
        return mark_safe(f'<a href="{enlace}" target="_blank">Ver Comisiones</a>')

    enlace_comisiones.short_description = 'Comisiones'
  
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','formatted_precio','cantidad','link_orden')
    
    def formatted_precio(self, obj):
        precio_formatted = f"{obj.precio:,.2f}".rstrip('0').rstrip('.')
        return format_html(f"${precio_formatted} COP")

    formatted_precio.short_description = 'Precio'

    
    @receiver(m2m_changed, sender=OrdenDeTrabajo.productos.through)
    def actualizar_inventario(sender, instance, action, **kwargs):
        if action == 'post_add':
            for producto_id in kwargs['pk_set']:
                producto = Producto.objects.get(id_producto=producto_id)
                producto.cantidad -= 1
                producto.save()
        elif action == 'post_remove':
            for producto_id in kwargs['pk_set']:
                producto = Producto.objects.get(id_producto=producto_id)
                producto.cantidad += 1
                producto.save()
                
    def link_orden(self, obj):
        ordenes = obj.ordendetrabajo_set.all()
        if ordenes:
            links = []
            for orden in ordenes:
                url = reverse("admin:authApp_ordendetrabajo_change", args=(orden.numero_orden,))
                link = f'<a href="{url}">{orden.numero_orden}</a>'
                links.append(link)
            return format_html(", ".join(links))
        return "-"

    link_orden.short_description = 'Número de Orden'     
    
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'formatted_precio')   
    
    def formatted_precio(self, obj):
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        formatted = locale.format_string('%d', obj.precio, grouping=True)
        formatted = formatted[:]  # Eliminar los dos ceros adicionales al final
        return f'${formatted}' 
    
    formatted_precio.short_description = 'Precio'  

    

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Operador)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Mpago)
admin.site.register(OrdenDeTrabajo, OrdenDeTrabajoAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Actividad)


