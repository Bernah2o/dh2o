import textwrap
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.decorators import action

from reportlab.lib.pagesizes import inch, A4
from reportlab.lib.units import cm
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from authApp.models.factura import Factura

from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = []  # Permite el acceso sin autenticación

    @action(detail=True, methods=['get'])
    def generar_reporte_pdf(self, request, reporte_id=None):
        # Obtener los datos del reporte
        reporte = get_object_or_404(Reporte, id_reporte=reporte_id)
        cliente = reporte.cliente

        # Crear el objeto PDF de ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte-{cliente.nombre.replace(" ", "-")}.pdf"'

        # Obtén los estilos de muestra
        styles = getSampleStyleSheet()

        # Crea un estilo personalizado con un tamaño de fuente más grande
        estilo_personalizado = ParagraphStyle(
            name='estilo_personalizado',
            parent=styles['Normal'],
            fontSize=12  # Tamaño de fuente deseado
        )

        # Modificar el estilo de título
        estilo_titulo = styles['Title']
        estilo_titulo.fontName = 'Helvetica-Bold'  # Cambia la fuente a Helvetica-Bold
        estilo_titulo.fontSize = 18  # Cambia el tamaño de fuente a 18 puntos
        estilo_titulo.textColor = colors.black  # Cambia el color del texto

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

        titulo_texto = f"<b>Informe de Actividades {reporte.orden_de_trabajo.numero_orden if reporte.orden_de_trabajo else ''}</b>"
        titulo = Paragraph(titulo_texto, estilo_titulo)

        # Crear una tabla con el logo y el título en dos columnas diferentes
        tabla_logo_titulo = Table([[logo_img, titulo]], colWidths=[100, 400])
        tabla_logo_titulo.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, 0), 'TOP'),  # Alinear el logo en la parte superior
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente todo el contenido de la tabla
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),  # Alinear el título al centro horizontalmente
        ]))

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
        imagen_despues_2 = Image(imagen_despues_2_path, width=2 * inch, height=2 * inch) if imagen_despues_2_path else None

        # Agregar los atributos del reporte
        tabla_datos = [
            ["Cliente:", f"{cliente.nombre} {cliente.apellido}"],
            ["Dirección:", cliente.direccion],
            ["Teléfono:", cliente.telefono],
            ["Fecha:", str(reporte.fecha)],
            ["Antes del lavado:", ""],
            ["", Table([[imagen_antes_1, Spacer(1, 0.5 * inch), imagen_antes_2]], colWidths=[2 * inch, 0.2 * inch, 2 * inch])],
            ["Después del lavado:", ""],
            ["", Table([[imagen_despues_1, Spacer(1, 0.5 * inch), imagen_despues_2]], colWidths=[2 * inch, 0.2 * inch])],
            ["Próxima Limpieza:", Paragraph(str(reporte.proxima_limpieza) if reporte.proxima_limpieza else "", estilo_personalizado)]
        ]

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
            spaceAfter=0,  # Ajustar el valor según sea necesario
            fontName="Helvetica",  # Ajustar la fuente según sea necesario
            fontSize=10,  # Ajustar el tamaño de fuente según sea necesario
        )

        # Agregar el texto de observación en la columna 0, fila 7
        observacion_text2 = "Estos tanques deben lavarse y desinfectarse mínimo cada seis meses,todo esto regido bajo los parámetros del Decreto 1575 de l9 de Mayo de 2007."
        observacion_text = "El agua almacenada puede verse afectada por condiciones ambientales y de temperatura, lo que podría comprometer su calidad y seguridad para el consumo humano. Es crucial asegurarse de que el agua que consumimos esté libre de contaminantes para prevenir enfermedades como el cólera, la tifoidea y la hepatitis A, entre otras."
        # Envolver el texto en párrafos y aplicar ajustes
        observacion_text2 = "\n".join(textwrap.wrap(observacion_text2, width=80))
        observacion_text = "\n".join(textwrap.wrap(observacion_text, width=80))
        # Crear el párrafo de observación con el estilo de tabla
        observacion2 = Paragraph(observacion_text2, estilo_justificado)
        observacion = Paragraph(observacion_text, estilo_justificado)

        # Agregar la observación a la tabla de datos en la posición correcta
        tabla_datos.append(["Nota:", observacion2])
        tabla_datos.append(["Importante:", observacion])
        # Añadir las líneas para mostrar las imágenes después del lavado
        tabla_datos.append(["Después del lavado:", ""])
        tabla_datos.append(["", Table([[imagen_despues_1, Spacer(1, 0.5 * inch), imagen_despues_2]], colWidths=[2 * inch, 0.2 * inch])])
        # Crear la tabla con los datos del reporte
        tabla = Table(tabla_datos, colWidths=[2 * inch, 5 * inch])
        # Establecer los estilos de la tabla
        tabla.setStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Añadir bordes a la tabla
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1eb8d1")),  # Establecer color de fondo para la primera fila
            ('BACKGROUND', (0, 7), (1, 7), colors.HexColor("#1eb8d1")),  # Establecer color de fondo para la fila 7
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Establecer tipo de letra y negrita para la primera fila
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinear el contenido de la primera fila al centro
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el contenido de la tabla
            ('SPAN', (0, 7), (1, 7)),  # Combinar la celda de la fila 7 en las columnas 0 y 1
            ('SPAN', (0, 4), (0, 7)),  # Combinar las celdas de la columna 0 desde la fila 4 hasta la fila 7
            ('SPLITBEFORE', (0, 7), (1, 7)),  # Mover la fila 8 a la siguiente página
        ])

        # Añadir estilo de alineación a las celdas combinadas
        tabla.setStyle([
            ('ALIGN', (0, 7), (1, 7), 'CENTER'),  # Alinear la celda combinada de la fila 7 a la derecha
        ])

        elements.append(tabla)

        # Agregar espacio en blanco
        elements.append(Spacer(1, 20))

        # Obtener el estilo de párrafo por defecto
        estilo_parrafo = styles['Normal']

        # Modificar el estilo para aplicar negrita
        estilo_parrafo.fontName = 'Helvetica-Bold'
        
        # Crear un estilo de párrafo con un tamaño de fuente más grande
        estilo_parrafo_grande = styles['Normal']
        estilo_parrafo_grande.fontSize = 14  # Tamaño de fuente deseado
        # Obtener el objeto OrdenDeTrabajo relacionado con el reporte
        orden_de_trabajo = reporte.orden_de_trabajo if reporte.orden_de_trabajo else None

        # Inicializar la variable para almacenar el total de la factura
        total_factura = 0

        if orden_de_trabajo:
            # Obtener la factura relacionada con la orden de trabajo
            factura = Factura.objects.filter(orden_de_trabajo=orden_de_trabajo).first()

            if factura:
                # Obtener el valor del campo "total" de la factura
                total_factura = factura.total

        # Crear un párrafo para mostrar el total en el PDF
        texto_total = "Total Servicio: ${:,.0f}".format(total_factura)
        parrafo_total = Paragraph(texto_total, estilo_parrafo)

        # Agregar el párrafo del total a la lista de elementos
        elements.append(parrafo_total)
        
        elements.append(Spacer(10, 30))

        # Definir una función para crear el hipervínculo con el logo
        def crear_hipervinculo_con_logo(url, texto, imagen):
            estilo_link = ParagraphStyle(
                "estilo_link",
                parent=styles["Normal"],
                textColor=colors.HexColor("#007bff"),  # Cambiar el color del hipervínculo (azul)
                underline=True,  # Agregar subrayado al hipervínculo
            )
            return f'<a href="{url}"><img src="{imagen}" height="20" width="20"></img> <font color="#007bff">{texto}</font></a>'

        
        # Rutas de los logos de las redes sociales
        logo_instagram = 'authApp/static/img/logo_instagram.png'
        logo_whatsapp = 'authApp/static/img/logo_whatsapp.png'
        logo_facebook = 'authApp/static/img/logo_facebook.png'

        # Crear la tabla con los hipervínculos y los logos
        tabla_redes_sociales = Table([
            [Paragraph(crear_hipervinculo_con_logo("https://www.instagram.com/dh2ocol/", "Instagram", logo_instagram)),
            Paragraph(crear_hipervinculo_con_logo("https://wa.me/3157484662", "WhatsApp", logo_whatsapp)),
            Paragraph(crear_hipervinculo_con_logo("https://www.facebook.com/dh2ocol/", "Facebook", logo_facebook))]
        ], colWidths=[2 * inch, 2 * inch, 2 * inch])

        # Establecer el estilo para centrar el contenido de la tabla
        tabla_redes_sociales.setStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el contenido de la tabla al centro
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el contenido de la tabla
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Agregar espacio inferior de 6 puntos en todas las celdas
        ])

        # Agregar la tabla de redes sociales a la lista de elementos
        elements.append(tabla_redes_sociales)


        # Agregar espacio en blanco
        elements.append(Spacer(1, 1))
             
        # Crear el documento PDF con ReportLab
        pdf.build(elements)

        return response
