import cgi
from rest_framework import viewsets
from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from reportlab.lib.utils import ImageReader
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

    def generar_reporte_pdf(request, self, reporte_id):
        # Obtener los datos del reporte
        reporte = Reporte.objects.get(id=reporte_id)
        # Generar el HTML del reporte
        html = render_to_string('pdf1.html', {'reporte': reporte})
    
        # Crear un archivo PDF en memoria
        result = BytesIO()
        pdf = pisa.CreatePDF(html.encode('UTF-8'), result)
    
        # Devolver el PDF generado como una respuesta HTTP
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte-{reporte.id}.pdf"'
            response['Content-Length'] = len(response.content)
            response['Cache-Control'] = 'no-cache'
            return response

        return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))