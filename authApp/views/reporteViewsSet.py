from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from authProject import settings
from authApp.models.reporte import Reporte  # Asegúrate de importar el modelo correcto
from weasyprint import HTML, CSS
import os
from django.template.loader import render_to_string
from authApp.serializers.reporteSerializers import ReporteSerializer
from rest_framework import viewsets


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = []  # Permite el acceso sin autenticación

    def generar_reporte_pdf(self, request, pk):
        reporte = get_object_or_404(Reporte, pk=pk)
        cliente = reporte.obtener_cliente()  # Ajusta el método según tu modelo

        context = {"reporte": reporte, "cliente": cliente}

        # Renderizar el HTML a partir de la plantilla
        html_string = render_to_string("reporte_template.html", context)

        # Crear una instancia de HTML a partir de una cadena de texto
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri())

        # Crear una instancia de CSS a partir de un archivo
        css_url = os.path.join(
            settings.BASE_DIR, "authApp/static/css/reporte.css"
        )  # Ajusta la ruta del archivo CSS
        css = CSS(filename=css_url)

        # Generar el archivo PDF
        pdf_file = html_obj.write_pdf(stylesheets=[css])

        # Devolver la respuesta HTTP con el archivo PDF
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="reporte-{cliente.nombre.replace(" ", "-")}.pdf"'
        return response
