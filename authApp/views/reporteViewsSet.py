import cgi
from rest_framework import viewsets, permissions
from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer
from datetime import timedelta


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    
    
    @staticmethod
    def generar_reporte_pdf(request,id_reporte):
        # Obtener los datos del reporte
        reporte = Reporte.objects.get(id=id_reporte)
        # Generar el HTML del reporte
        html = render_to_string('pdf1.html', {'reporte': reporte})
    
        # Crear un archivo PDF en memoria
        result = BytesIO()
        pdf = pisa.CreatePDF(html.encode('UTF-8'), result)
    
        # Devolver el PDF generado como una respuesta HTTP
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte-{id_reporte}.pdf"'
            response['Content-Length'] = len(response.content)
            response['Cache-Control'] = 'no-cache'
            return response

        return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
    