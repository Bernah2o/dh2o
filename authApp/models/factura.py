from django.db import models
from django.template.loader import render_to_string


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
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura {self.numero_factura}"

    def save(self, *args, **kwargs):
        self.total = self.orden_de_trabajo.calcular_total() - self.descuento
        super().save(*args, **kwargs)

        self.orden_de_trabajo.facturada = True
        self.orden_de_trabajo.save()

    @property
    def cliente(self):
        return self.orden_de_trabajo.cliente

    def generar_html_factura(self):
        context = {"factura": self}
        html = render_to_string("factura_template.html", context)
        return html
