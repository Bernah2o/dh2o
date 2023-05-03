from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas


def generate_pdf(reporte):
    # Crear un buffer de memoria para guardar el PDF
    buffer = BytesIO()

    # Crear un objeto PDF usando el buffer como su "archivo"
    p = canvas.Canvas(buffer)

    # Definir el contenido del PDF usando la información del reporte
    p.drawString(100, 750, "Reporte")
    p.drawString(100, 700, "ID: {}".format(reporte.id))
    p.drawString(100, 650, "Orden de trabajo: {}".format(reporte.orden_de_trabajo))
    p.drawString(100, 600, "Fecha: {}".format(reporte.fecha))
    p.drawString(100, 550, "Descripción: {}".format(reporte.descripcion))
    
    # Aquí puedes agregar más información al reporte utilizando ReportLab

    # Cerrar el objeto PDF
    p.showPage()
    p.save()

    # Obtener el valor del buffer de memoria y crear la respuesta HTTP
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte-{}.pdf"'.format(reporte.id)
    return response

generate_pdf.short_description = "Imprimir PDF"
