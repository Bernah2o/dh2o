import datetime
from io import BytesIO
import os
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from PIL import Image
from dateutil.relativedelta import relativedelta
from django.db import models
from authApp.models.ordendetrabajo import OrdenDeTrabajo
from authProject import settings
from datetime import datetime


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateField()
    imagen_antes_lavado_1 = models.ImageField(upload_to="reportes/", null=True)
    imagen_antes_lavado_2 = models.ImageField(upload_to="reportes/", null=True)
    imagen_despues_lavado_1 = models.ImageField(upload_to="reportes/", null=True)
    imagen_despues_lavado_2 = models.ImageField(upload_to="reportes/", null=True)
    proxima_limpieza = models.DateField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.orden_de_trabajo.numero_orden}"

    def estandarizar_imagen(self, imagen_path, nuevo_tamano=(960, 960)):
        if imagen_path:
            try:
                # Abre la imagen usando PIL
                with Image.open(imagen_path) as img:
                    print(f"Tamaño original de la imagen: {img.size}")
                    # Ajusta el tamaño
                    img.thumbnail(nuevo_tamano)  # Ajusta el tamaño
                    print(f"Tamaño después del ajuste: {img.size}")

                # Genera una nueva ruta para la imagen estandarizada
                nueva_ruta_estandarizada = os.path.join(
                    self.generar_ruta_estandarizada(imagen_path)
                )
                print(f"Nueva ruta estandarizada: {nueva_ruta_estandarizada}")

                # Guarda la imagen estandarizada
                img.save(nueva_ruta_estandarizada)
                print("Imagen estandarizada con éxito")

                # Devuelve la ruta de la imagen estandarizada
                return nueva_ruta_estandarizada

            except Exception as e:
                print(f"Error al estandarizar la imagen: {e}")
                raise RuntimeError(f"Error al estandarizar la imagen: {e}")
        else:
            print(f"La ruta de la imagen no existe: {imagen_path}")
            # Puedes realizar alguna acción adicional o lanzar una excepción según tus necesidades

    def generar_ruta_estandarizada(self, imagen_path):
        _, extension = os.path.splitext(imagen_path)        
        directorio_estandarizado = os.path.join(
            settings.BASE_DIR, "authApp", "media", "reportes", "estandarizadas"
        )
        print(f"Directorio estandarizado: {directorio_estandarizado}")

        # Crea el directorio si no existe
        os.makedirs(directorio_estandarizado, exist_ok=True)
        print(f"Directorio creado correctamente: {directorio_estandarizado}")

        # Genera una nueva ruta basada en el ID del reporte y un timestamp único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # formato: YYYYMMDDHHMMSSmicro
        nueva_ruta = os.path.join(
            directorio_estandarizado, f"{self.id_reporte}_{timestamp}{extension}"
        )

        return nueva_ruta

    def save(self, *args, **kwargs):
        # Calcula la fecha de próxima limpieza sumando 6 meses a la fecha actual
        if not self.proxima_limpieza:
            self.proxima_limpieza = self.fecha + relativedelta(months=6)
        super().save(
            *args, **kwargs
        )  # Guardar primero para obtener la ruta de la imagen

        
        # Estandarizar las imágenes antes de guardarlas
        if self.imagen_antes_lavado_1:
            self.imagen_antes_lavado_1 = self.estandarizar_imagen(
                self.imagen_antes_lavado_1.path
            )
        if self.imagen_antes_lavado_2:
            self.imagen_antes_lavado_2 = self.estandarizar_imagen(
                self.imagen_antes_lavado_2.path
            )
        if self.imagen_despues_lavado_1:
            self.imagen_despues_lavado_1 = self.estandarizar_imagen(
                self.imagen_despues_lavado_1.path
            )
        if self.imagen_despues_lavado_2:
            self.imagen_despues_lavado_2 = self.estandarizar_imagen(
                self.imagen_despues_lavado_2.path
            )

    def generar_pdf(request, reporte_id):
        reporte = get_object_or_404(Reporte, id_reporte=reporte_id)

        # Estandarizar las imágenes justo antes de generar el PDF
        estandarizar_antes_lavado_1 = reporte.estandarizar_imagen(
            reporte.imagen_antes_lavado_1.path, nuevo_tamano=(960, 960)
        )
        estandarizar_antes_lavado_2 = reporte.estandarizar_imagen(
            reporte.imagen_antes_lavado_2.path, nuevo_tamano=(960, 960)
        )
        estandarizar_despues_lavado_1 = reporte.estandarizar_imagen(
            reporte.imagen_despues_lavado_1.path, nuevo_tamano=(960, 960)
        )
        estandarizar_despues_lavado_2 = reporte.estandarizar_imagen(
            reporte.imagen_despues_lavado_2.path, nuevo_tamano=(960, 960)
        )
        
        # Ruta de la plantilla HTML
        template_path = "authApp/reporte_template.html"
        template = get_template(template_path)

        # Contexto para la plantilla
        context = {
            "reporte": reporte,
            "estandarizar_antes_lavado_1": estandarizar_antes_lavado_1,
            "estandarizar_antes_lavado_2": estandarizar_antes_lavado_2,
            "estandarizar_despues_lavado_1": estandarizar_despues_lavado_1,
            "estandarizar_despues_lavado_2": estandarizar_despues_lavado_2,
        }

        # Renderizar la plantilla con el contexto
        html = template.render(context)

        try:
            # Crear el PDF usando xhtml2pdf
            pdf_response = HttpResponse(content_type="application/pdf")
            pdf_response["Content-Disposition"] = f'filename="{reporte.id_reporte}.pdf"'
            pisa.CreatePDF(BytesIO(html), dest=pdf_response)

            # Si la generación del PDF fue exitosa, devuelve la respuesta
            return pdf_response

        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            raise RuntimeError(f"Error al generar el PDF: {e}")

    def obtener_cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    obtener_cliente.short_description = "Cliente asociado"

    def total_servicio(self):
        return self.orden_de_trabajo.calcular_total()

    @property
    def cliente(self):
        if self.orden_de_trabajo:
            return self.orden_de_trabajo.cliente
        return None

    @staticmethod
    def buscar_por_cliente(cliente_id):
        return Reporte.objects.filter(orden_de_trabajo__cliente__id=cliente_id)
