from django.db import models
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError


class Factura(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    fecha = models.DateField()
    orden_de_trabajo = models.ForeignKey(
        "authApp.OrdenDeTrabajo",
        on_delete=models.CASCADE,
        limit_choices_to={"factura__isnull": True},
    )
    mpago = models.ForeignKey("authApp.Mpago", on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, editable=False
    )  # Campo para almacenar el total de la factura

    def __str__(self):
        return f"Factura {self.numero_factura}"

    def clean(self):
        if Factura.objects.filter(numero_factura=self.numero_factura).exists():
            raise ValidationError("El número de factura debe ser único.")

    def calcular_total(self):
        total_orden_trabajo = (
            self.orden_de_trabajo.calcular_total()
        )  # Obtener el total de la orden de trabajo
        return (
            total_orden_trabajo - self.descuento
        )  # Restar el descuento y retornar el total de la factura

    def save(self, *args, **kwargs):
        if not self.pk:
            last_invoice = Factura.objects.order_by("-pk").first()
            self.pk = last_invoice.pk + 1 if last_invoice else 1

        super().save(*args, **kwargs)

        self.orden_de_trabajo.facturada = True
        self.orden_de_trabajo.save()

    @property
    def cliente(self):
        return self.orden_de_trabajo.cliente

    def generar_html_factura(self):
        context = {"factura": self}
        html = render_to_string("factura.html", context)
        return html
