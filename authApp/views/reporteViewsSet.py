import io
from django.http import FileResponse, HttpResponse
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer
import xhtml2pdf.pisa as pisa

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

    def generar_reporte(self, pk):
        reporte = Reporte.objects.get(pk=pk)
        # Lógica para generar el archivo HTML utilizando ReportLab

        template = get_template('authApp/template/reporte.html')
        context = {'reporte': reporte}
        html = template.render(context)

        # Convertir el archivo HTML a PDF utilizando xhtml2pdf
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), pdf_file)
        pdf = pdf_file.getvalue()
        pdf_file.close()

        # Devolver la respuesta HTTP con el archivo PDF generado
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        response.write(pdf)

        return response

    @action(detail=True, methods=['get'])
    @csrf_exempt
    def imprimir_reporte(self, request, pk=None):
        response = self.generar_reporte(pk)
        return response

   