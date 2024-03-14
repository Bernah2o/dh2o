from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authProject import settings
from authApp.models.reporte import Reporte  # Asegúrate de importar el modelo correcto
from weasyprint import HTML, CSS
import os
from authApp.serializers.reporteSerializers import ReporteSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = []  # Permite el acceso sin autenticación

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["orden_de_trabajo_instance"] = OrdenDeTrabajo.objects.get(
            pk=self.kwargs["orden_de_trabajo_id"]
        )
        return kwargs

    def create(self, request, *args, **kwargs):
        form = self.get_form(request, data=request.data)
        if form.is_valid():
            # Obtener la instancia de la orden de trabajo desde el formulario
            orden_de_trabajo = form.cleaned_data["orden_de_trabajo"]
            # Guardar un reporte para cada servicio seleccionado en el formulario
            for servicio_en_orden in form.cleaned_data["servicio_en_orden"]:
                reporte = form.save(commit=False)
                reporte.orden_de_trabajo = orden_de_trabajo
                reporte.servicio_en_orden = servicio_en_orden
                reporte.save()
            serializer = self.get_serializer(reporte)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.get_form(request, instance=instance, data=request.data)
        if form.is_valid():
            reporte = form.save()
            serializer = self.get_serializer(reporte)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def generar_pdf(self, request, pk):
        reporte = get_object_or_404(Reporte, pk=pk)

        # Obtener el servicio en orden asociado al reporte
        servicio_en_orden = reporte.servicio_en_orden

        # Si no hay un servicio en orden asociado, retornar un error
        if not servicio_en_orden:
            return HttpResponse("No se ha seleccionado un servicio en orden asociado al reporte.")

        # Obtener información del servicio en orden
        servicio = servicio_en_orden.servicio
        nombre_servicio = servicio.nombre
        cantidad_servicio = servicio_en_orden.cantidad_servicio
        precio_servicio = servicio.precio

        # Obtener información adicional del reporte
        cliente = reporte.orden_de_trabajo.cliente

        # Crear el contexto para la plantilla
        context = {
            "reporte": reporte,
            "cliente": cliente,
            "servicio": {
                "nombre": nombre_servicio,
                "cantidad": cantidad_servicio,
                "precio": precio_servicio,
            },
        }

        # Renderizar la plantilla HTML
        template_path = "reporte_template.html"
        template = get_template(template_path)
        html_string = template.render(context)

        # Convertir el HTML a PDF
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri())
        css_url = os.path.join(settings.BASE_DIR, "authApp/static/css/reporte.css")
        css = CSS(filename=css_url)
        pdf_file = html_obj.write_pdf(stylesheets=[css])

        # Preparar la respuesta con el PDF
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte-{cliente.nombre.replace(" ", "-")}.pdf"'
        return response
