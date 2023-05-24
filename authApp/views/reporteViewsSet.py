from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import action

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer
class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [] # Permite el acceso sin autenticación
        
    @action(detail=True, methods=['get'])
    def generar_reporte_pdf(self, request, reporte_id=None):
        # Obtener los datos del reporte
        reporte = get_object_or_404(Reporte, id_reporte=reporte_id)
        
        # Obtener las actividades desarrolladas del reporte
        actividades_desarrolladas = [dict(Reporte.ACTIVIDADES_CHOICES).get(actividad) for actividad in reporte.actividades_desarrolladas]
        
        # Crear el objeto PDF de ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte-{reporte_id}.pdf"'

        # Crear el documento PDF con ReportLab
        pdf = SimpleDocTemplate(response, pagesize=letter)

        # Crear una lista para almacenar los elementos del documento
        elements = []

        # Agregar el logo al documento
        logo_path = 'authApp/static/img/logo.png'  # Ruta a tu archivo de imagen del logo
        logo = utils.ImageReader(logo_path)
        logo_width, logo_height = logo.getSize()
        logo_aspect = logo_height / logo_width
        logo_img = Image(logo_path, width=100, height=100 * logo_aspect)
        elements.append(logo_img)

        # Estilos de texto
        styles = getSampleStyleSheet()
        estilo_titulo = styles['Title']
        estilo_parrafo = styles['Normal']
        estilo_tabla = ParagraphStyle('tabla', parent=styles['Normal'], alignment=TA_LEFT)

        # Agregar el título del reporte
        titulo = Paragraph(f"<b>Reporte {reporte.orden_de_trabajo.numero_orden}</b>", estilo_titulo)
        elements.append(titulo)
        elements.append(Spacer(1, 20))
        
        # Obtener las imágenes de antes del lavado
        imagen_antes_1_path = reporte.imagen_antes_lavado_1.path if reporte.imagen_antes_lavado_1 else None
        imagen_antes_2_path = reporte.imagen_antes_lavado_2.path if reporte.imagen_antes_lavado_2 else None

        # Crear las imágenes de antes del lavado con las dimensiones deseadas
        imagen_antes_1 = Image(imagen_antes_1_path, width=2 * inch, height=2 * inch) if imagen_antes_1_path else None
        imagen_antes_2 = Image(imagen_antes_2_path, width=2 * inch, height=2 * inch) if imagen_antes_2_path else None

        # Obtener las imágenes de después del lavado
        imagen_despues_1_path = reporte.imagen_despues_lavado_1.path if reporte.imagen_despues_lavado_1 else None
        imagen_despues_2_path = reporte.imagen_despues_lavado_2.path if reporte.imagen_despues_lavado_2 else None

        # Crear las imágenes de después del lavado con las dimensiones deseadas
        imagen_despues_1 = Image(imagen_despues_1_path, width=2 * inch, height=2 * inch) if imagen_despues_1_path else None
        imagen_despues_2 = Image(imagen_despues_2_path, width=2 * inch, height=2 * inch) if imagen_despues_2_path else None 
        
                
        # Agregar los atributos del reporte
        tabla_datos = [
            ["Orden de Trabajo:", reporte.orden_de_trabajo.numero_orden],
            ["Cliente:", f"{reporte.cliente.nombre} {reporte.cliente.apellido}"],
            ["Dirección:", reporte.cliente.direccion],
            ["Teléfono:", reporte.cliente.telefono],
            ["Fecha:", str(reporte.fecha)],
            # Agregar la columna "Actividades Desarrolladas" con sus descripciones
            ["Actividades Desarrolladas:", "Inspección y riesgos: Identificar peligros y riesgos en el área."],
            ["", "Cierre de entrada y salida: Verificar cierre para evitar ingreso de agua."],
            ["", "Equipos de protección personal (EPP): Asegurar EPP necesarios."],
            ["", "Bombeo y aspirado: Retirar agua del tanque con equipo."],
            ["", "Limpieza del fondo: Remover sedimentos y residuos del fondo."],
            ["", "Limpieza a presión: Limpiar paredes y techos con alta presión."],
            ["", "Aspirado de residuos: Retirar agua sucia y residuos del tanque."],
            ["", "Inspección final: Verificar limpieza y preparación para desinfección."],
            ["Imágenes de antes del lavado:", ""],
            ["", imagen_antes_1],
            ["", imagen_antes_2],
            ["Imágenes de después del lavado:", ""],
            ["", imagen_despues_1],
            ["", imagen_despues_2],
        ]   # Agregar más filas para las demás actividades
        
         

        tabla = Table(tabla_datos, style=[
            ('GRID', (0, 0), (-1, -1), 1, 'black'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
        ])

        tabla.setStyle(TableStyle([
            
            ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            
        ]))
        
        elements.append(tabla)

        # Agregar espacio en blanco
        elements.append(Spacer(1, 20))

        
        
        # Agregar los elementos al documento PDF
        pdf.build(elements)

        return response

  
  
  
  
  
  
    """@staticmethod
    def generar_reporte_pdf(request, reporte_id):
        # Obtener los datos del reporte
        reporte = get_object_or_404(Reporte, id_reporte=reporte_id)
        
        # Obtener las actividades desarrolladas del reporte
        actividades_desarrolladas = reporte.actividades_desarrolladas

        # Obtener las URL de las imágenes
        imagen_antes_url = reporte.imagen_antes_lavado.url if reporte.imagen_antes_lavado else None
        imagen_despues_url = reporte.imagen_despues_lavado.url if reporte.imagen_despues_lavado else None
        
        # Generar el contenido HTML del reporte
        html_string = render_to_string('pdf_template.html', {
            'reporte': reporte,
            'actividades_desarrolladas': actividades_desarrolladas,
            'imagen_antes_url': imagen_antes_url,
            'imagen_despues_url': imagen_despues_url
        })

         # Definir el buscador de URL personalizado
        def url_fetcher(url):
            if url.startswith('{{ MEDIA_URL }}'):
                # Eliminar el prefijo '{{ MEDIA_URL }}' de la URL
                url = url[len('{{ MEDIA_URL }}'):]
                 # Construir la ruta completa utilizando la configuración de archivos multimedia
                url = os.path.join(settings.MEDIA_ROOT, url)
                # Ajustar 'mime_type' según el tipo de imagen que estés utilizando
                mime_type = 'image/jpeg'  # Ejemplo: imágenes en formato JPEG
                return dict(string=url, mime_type=mime_type)
            return default_url_fetcher(url)

        # Crear el objeto HTML de WeasyPrint con el buscador personalizado
        html = HTML(string=html_string, url_fetcher=url_fetcher)

        # Generar el PDF
        pdf_file = html.write_pdf()

        # Devolver el PDF generado como una respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte-{reporte_id}.pdf"'
        response['Content-Length'] = len(pdf_file)
        response.write(pdf_file)

        return response """""
    
    
    """@staticmethod
    def generar_reporte_pdf(request,reporte_id):
        # Obtener los datos del reporte
        reporte = Reporte.objects.get(id_reporte=reporte_id)
        # Generar el HTML del reporte
        html = render_to_string('pdf1.html', {'reporte': reporte})
    
        # Crear un archivo PDF en memoria
        result = BytesIO()
        pdf = pisa.CreatePDF(html.encode('UTF-8'), result)
    
        # Devolver el PDF generado como una respuesta HTTP
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte-{reporte_id}.pdf"'
            response['Content-Length'] = len(response.content)
            response['Cache-Control'] = 'no-cache'
            return response

        return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
        """
    