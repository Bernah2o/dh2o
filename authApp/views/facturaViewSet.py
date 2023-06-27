
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from django.db.models import Sum    
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import os


from authApp.models.factura import Factura
from authApp.serializers.facturaSerializer import FacturaSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [] # Permite el acceso sin autenticación
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
        
    @action(detail=False, methods=['get'])
    def ventas_mensuales(self, request):
        year = datetime.now().year
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        ventas_mensuales = []

        for mes in range(1, 13):
            total_ventas = Factura.objects.filter(fecha__year=year, fecha__month=mes).aggregate(total=Sum('total'))['total']
            ventas_mensuales.append((mes, meses[mes-1], total_ventas or 0))
        
        return render(request, 'ventas_mensuales.html', {'ventas_mensuales': ventas_mensuales})
    
    
    def generar_factura(request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        context = {'factura': factura}

        # Renderizar el HTML a partir de la plantilla
        html_string = render_to_string('factura_template.html', context)

        # Crear una instancia de HTML a partir de una cadena de texto
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri())

        # Crear una instancia de CSS a partir de un archivo
        css_url = os.path.join(settings.BASE_DIR, 'authApp/static/css/factura.css')
        css = CSS(filename=css_url)

        # Generar el archivo PDF
        pdf_file = html_obj.write_pdf(stylesheets=[css])

        # Devolver la respuesta HTTP con el archivo PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
        return response
                
        
   
    """@staticmethod
    def generar_factura(request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        context = {'factura': factura}
        html = render_to_string('factura_template.html', context)
        return HttpResponse(html)"""
