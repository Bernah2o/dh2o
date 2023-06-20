import textwrap
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.decorators import action

from reportlab.lib.pagesizes import inch
#from reportlab.lib.units import inch

from reportlab.platypus import Image
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import re

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
        
        # Obtener el nombre y apellido del cliente
        cliente = reporte.cliente
        nombre_cliente = cliente.nombre.replace(" ", "-")
        apellido_cliente = cliente.apellido.replace(" ", "-")
        # Crear el objeto PDF de ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte-{nombre_cliente}.pdf"'
        
        # Obtén los estilos de muestra
        styles = getSampleStyleSheet()

        # Crea un estilo personalizado con un tamaño de fuente más grande
        estilo_personalizado = ParagraphStyle(
            name='estilo_personalizado',
            parent=styles['Normal'],
            fontSize=12  # Tamaño de fuente deseado
        )
            
        # Obtener los estilos de muestra
        styles = getSampleStyleSheet()

        # Modifica el estilo de título  
        estilo_titulo = styles['Title']
        estilo_titulo.fontName = 'Helvetica-Bold'  # Cambia la fuente a Helvetica-Bold
        estilo_titulo.fontSize = 18  # Cambia el tamaño de fuente a 18 puntos
        estilo_titulo.textColor = colors.black  # Cambia el color del texto 
                
        # Estilo de párrafo
        estilo_parrafo = styles['Normal']

        estilo_tabla = ParagraphStyle('tabla', parent=styles['Normal'], alignment=TA_LEFT)
        
        # Crear el documento PDF con ReportLab
        pdf = SimpleDocTemplate(response, pagesize=A4, leftMargin=3 * cm, rightMargin=3 * cm, topMargin=1.0 * cm, bottomMargin=1.0 * cm)
        
        # Crear una lista para almacenar los elementos del documento
        elements = []
        
        # Agregar el logo al documento
        logo_path = 'authApp/static/img/logo.png'  # Ruta a tu archivo de imagen del logo
        logo = utils.ImageReader(logo_path)
        logo_width, logo_height = logo.getSize()
        logo_aspect = logo_height / logo_width
        logo_img = Image(logo_path, width=100, height=100 * logo_aspect)
        
        titulo_texto = "<b>Actividades de Limpieza de Tanques Elevados</b>"
        if reporte.orden_de_trabajo is not None:
            titulo_texto += f" {reporte.orden_de_trabajo.numero_orden}"

        titulo = Paragraph(titulo_texto, estilo_titulo)
        
        # Crear una tabla con el logo y el título
        tabla_logo_titulo = Table([[logo_img, titulo]], colWidths=[100, 400])
        tabla_logo_titulo.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))# Alinear verticalmente al principio (parte superior)
        
        # Alinear el título horizontalmente al centro
        titulo.alignment = 1  # 0 para izquierda, 1 para centro, 2 para derecha

        elements.append(Spacer(1, 20))
        elements.append(tabla_logo_titulo)
        elements.append(Spacer(1, 1))
        
           
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
        imagen_despues_2 = Image(imagen_despues_2_path, width=2 * inch, height=1 * inch) if imagen_despues_2_path else None 
                        
        # Agregar los atributos del reporte
        tabla_datos = [
            
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
            ["Antes del lavado:", ""],
            ["", Table([[imagen_antes_1, Spacer(1, 0.5 * inch), imagen_antes_2]], colWidths=[2 * inch, 0.2 * inch, 2 * inch])],
            ["Después del lavado:", ""],
            ["", Table([[imagen_despues_1,Spacer(1, 0.5 * inch), imagen_despues_2]], colWidths=[2 * inch, 0.2 * inch])],
            ["Próxima Limpieza:", Paragraph(str(reporte.proxima_limpieza) if reporte.proxima_limpieza else "", estilo_personalizado)],
            
            
        ]   # Agregar más filas para las demás actividades
        
            
        # Obtener los estilos de muestra
        styles = getSampleStyleSheet()

        # Crear un estilo personalizado para justificar el texto
        estilo_justificado = ParagraphStyle(
            "estilo_justificado",
            parent=styles["Normal"],
            alignment=TA_JUSTIFY if hasattr(TA_JUSTIFY, 'name') else 4,  # Using 4 for JUSTIFY if TA_JUSTIFY is not available
            leftIndent=1,  # Ajustar el valor según sea necesario
            rightIndent=1,  # Ajustar el valor según sea necesario
            spaceBefore=0,  # Ajustar el valor según sea necesario
            spaceAfter=0,   # Ajustar el valor según sea necesario
            fontName="Helvetica",  # Ajustar la fuente según sea necesario
            fontSize=10,  # Ajustar el tamaño de fuente según sea necesario
                
        )

        # Agregar el texto de observación en la columna 0, fila 12
        observacion_text2 = "Nota: Estos tanques deben lavarse y desinfectarse mínimo cada seis meses,todo esto regido bajo los parámetros del Decreto 1575 de l9 de Mayo de 2007."
        observacion_text = "Importante: El agua almacenada puede verse afectada por condiciones ambientales y de temperatura, lo que podría comprometer su calidad y seguridad para el consumo humano. Es crucial asegurarse de que el agua que consumimos esté libre de contaminantes para prevenir enfermedades como el cólera, la tifoidea y la hepatitis A, entre otras."
        
        # Envolver el texto en párrafos y aplicar ajustes
        observacion_text2 = "\n".join(textwrap.wrap(observacion_text2, width=80))
        observacion_text = "\n".join(textwrap.wrap(observacion_text, width=80))
        # Crear el párrafo de observación con el estilo de tabla
        observacion2 = Paragraph(observacion_text2, estilo_justificado)
        observacion = Paragraph(observacion_text, estilo_justificado)
        
        # Agregar la observación a la tabla de datos en la posición correcta
        tabla_datos[15][0] = observacion2
        tabla_datos[13][0] = observacion
        
       
        # Crear la tabla con los datos del reporte
        tabla = Table(tabla_datos, colWidths=[2 * inch, 5 * inch])
        
        # PALETA DE COLORES DH2O
        color = colors.HexColor("#1eb8d1") # AZUL 2
        color1 = colors.HexColor("#1986c8") # AZUL 
        color2 = colors.HexColor("#008037") # VERDE

        # Establecer los estilos de la tabla
        tabla.setStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Añadir bordes a la tabla
            ('BACKGROUND', (0, 0), (-1, 0), color),  # Establecer color de fondo para la primera fila
            ('BACKGROUND', (0, 16), (1, 16), color), # Establecer color de fondo para la fila 16
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Establecer tipo de letra y negrita para la primera fila
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinear el contenido de la primera fila al centro
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el contenido de la tabla
            ('SPAN', (0, 12), (1, 12)),  # Combinar la celda de la fila 12 en las columnas 0 y 1
            ('SPAN', (0, 14), (1, 14)), # Combinar la celda de la fila 14 en las columnas 0 y 1
            ('SPAN', (0, 4), (0, 11)), # Combinar las celdas de la columna 0 desde la fila 4 hasta la fila 11
            ('SPLITBEFORE', (0, 12), (1, 12)),  # Mover la fila 13 a la siguiente página
                    
        ])
        
        
        # Añadir estilo de alineación a las celdas combinadas
        tabla.setStyle([
            ('ALIGN', (0, 12), (1, 12), 'CENTER'),  # Alinear la celda combinada de la fila 13 a la derecha
            ('ALIGN', (0, 14), (1, 14), 'CENTER'),  # Alinear la celda combinada de la fila 14 a la derecha
        ])  
           
        elements.append(tabla)

        # Agregar espacio en blanco
        elements.append(Spacer(1, 20))
        
        # Agregar el texto adicional al final del PDF
        #texto_adicional = "MINISTERIO DE LA PROTECCION SOCIAL DECRETO NÚMERO 1575 DE 2007 (Mayo 9) CAPITULO III ARTÍCULO 10º.- RESPONSABILIDAD DE LOS USUARIOS. Todo usuario es responsable de mantener en condiciones sanitarias adecuadas las instalaciones de distribución y almacenamiento de agua para consumo humano a nivel intradomiciliario."
        #texto = Paragraph(texto_adicional, estilo_parrafo)
        
        #elements.append(texto)
    
        # Agregar espacio en blanco
        elements.append(Spacer(1, 1))

        # Obtener el estilo de párrafo por defecto
        styles = getSampleStyleSheet()
        estilo_parrafo = styles['Normal']

        # Modificar el estilo para aplicar negrita
        estilo_parrafo.fontName = 'Helvetica-Bold'
        
        
        # Definir una función para crear el hipervínculo con el logo
        def crear_hipervinculo_con_logo(url, texto, imagen):
            return f'<a href="{url}"><img src="{imagen}" height="16" width="16"></img>{texto}</a>'

        # Rutas de los logos de las redes sociales
        logo_instagram = 'authApp/static/img/logo_instagram.png'
        logo_whatsapp = 'authApp/static/img/logo_whatsapp.png'
        logo_facebook = 'authApp/static/img/logo_facebook.png'

        # Crear el texto con los hipervínculos y los logos
        # Crear el texto con los hipervínculos y los logos
        agradecimiento = 'Siguenos en nuestras redes sociales ' \
                 f'{crear_hipervinculo_con_logo("https://www.instagram.com/dh2ocol/", "Instagram", logo_instagram)}\n\n' \
                 f'{crear_hipervinculo_con_logo("https://wa.me/3157484662",  "WhatsApp", logo_whatsapp)}\n\n' \
                 f'{crear_hipervinculo_con_logo("https://www.facebook.com/dh2ocol/", "Facebook", logo_facebook)}' 

        # Crear el párrafo con el texto y el estilo
        texto_agradecimiento = Paragraph(agradecimiento, estilo_parrafo)
        # Agregar el párrafo a la lista de elementos
        elements.append(texto_agradecimiento)
               
        # Agregar los elementos al documento PDF
        pdf.build(elements)
        

        return response
    
    def obtener_cliente(request, reporte_id):
        # Obtén una instancia de Reporte
        reporte = Reporte.objects.get(id_reporte=reporte_id)

        # Accede al cliente asociado a través de la propiedad cliente
        cliente_asociado = reporte.cliente

        # Realiza alguna operación con el cliente asociado
        # ...

        return render(request, 'tu_template.html', {'cliente': cliente_asociado})

  
   
  
  
  
    