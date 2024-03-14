from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from authApp.forms import ReporteForm
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authProject import settings
from authApp.models.reporte import Reporte  # Asegúrate de importar el modelo correcto
from weasyprint import HTML, CSS
import os
from django.db.models import Count
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
        form = ReporteForm(request.data)
        if form.is_valid():
            reporte = form.save()
            orden_de_trabajo = reporte.orden_de_trabajo
            if self.verificar_orden_de_trabajo_completa(orden_de_trabajo):
                return Response(
                    {"message": "La orden de trabajo se ha completado"},
                    status=status.HTTP_201_CREATED,
                )
            serializer = self.get_serializer(reporte)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        form = ReporteForm(request.data, instance=instance)
        if form.is_valid():
            reporte = form.save()
            orden_de_trabajo = reporte.orden_de_trabajo
            if self.verificar_orden_de_trabajo_completa(orden_de_trabajo):
                return Response({"message": "La orden de trabajo se ha completado"})
            serializer = self.get_serializer(reporte)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def verificar_orden_de_trabajo_completa(self, orden_de_trabajo):
        total_servicios = orden_de_trabajo.servicios_en_orden_detalle.count()
        servicios_con_reporte = orden_de_trabajo.servicios_en_orden_detalle.annotate(
            num_reportes=Count('reporte')
        ).filter(num_reportes__gt=0).count()
        
        if total_servicios == servicios_con_reporte:
            orden_de_trabajo.completa = True
            orden_de_trabajo.save()
            return True
        return False

    def get_form(self):
        form = super().get_form()
        if "orden_de_trabajo_instance" in self.kwargs:
            orden_de_trabajo_instance = self.kwargs["orden_de_trabajo_instance"]
            # Filtrar las órdenes de trabajo que no están completas
            ordenes_no_completas = OrdenDeTrabajo.objects.exclude(
                id=orden_de_trabajo_instance.id
            ).filter(completa=False)

            # Filtrar las órdenes que tienen servicios pendientes
            servicios_pendientes = orden_de_trabajo_instance.servicios_en_orden_detalle.filter(
                reporte__isnull=True
            )
            ordenes_no_completas = ordenes_no_completas.annotate(
                num_reportes=Count("servicios_en_orden_detalle__reporte")
            ).filter(num_reportes__lt=servicios_pendientes.count())

            # Aplicar la exclusión al queryset del formulario
            form.fields["orden_de_trabajo"].queryset = ordenes_no_completas
        return form


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
