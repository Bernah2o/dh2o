from django.db import models, transaction
from decimal import Decimal
from django.core.exceptions import ValidationError
from authApp.models.factura import Factura
from authApp.models.producto import Producto
from authApp.models.servicios import Servicio

import logging

# Configurar el logger para que imprima mensajes de depuración
logger = logging.getLogger(__name__)


class OrdenDeTrabajo(models.Model):
    numero_orden = models.AutoField(primary_key=True, verbose_name="Número de Orden")
    fecha = models.DateField()
    cliente = models.ForeignKey("authApp.Cliente", on_delete=models.CASCADE)
    operador = models.ForeignKey("authApp.Operador", on_delete=models.CASCADE)
    descripcion = models.TextField()
    facturada = models.BooleanField(default=False)
    servicios_en_orden = models.ManyToManyField(
        "Servicio",
        through="ServicioEnOrden",
        related_name="ordenes_de_trabajo",
        blank=True,
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=False
    )  # Campo no editable

    def __str__(self):
        return f" {self.numero_orden} - Cliente: {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto no tiene clave primaria asignada (es nuevo)
            ultimo_numero_orden = (
                OrdenDeTrabajo.objects.order_by("-numero_orden")
                .values_list("numero_orden", flat=True)
                .first()
            )
            self.numero_orden = ultimo_numero_orden + 1 if ultimo_numero_orden else 1
        # Calcular el total antes de guardar
        self.total = self.calcular_total()

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk:
            existing_facturas = Factura.objects.filter(orden_de_trabajo=self)
            if existing_facturas.exists():
                raise ValidationError(
                    "Esta orden de trabajo ya tiene una factura asociada."
                )
    def calcular_comision(self):
            try:
                # Obtener la suma total de los precios de todos los servicios en la orden de trabajo
                total_servicios = self.calcular_total()

                # Calcular la comisión como el 10% de la suma total de servicios
                comision = total_servicios * Decimal("0.1")

                # Si la comisión es mayor que cero, agregarla al operador y guardar
                if comision > 0:
                    self.operador.comisiones += comision
                    self.operador.save()

                # Lógica adicional cuando la comisión es cero
                if comision == 0:
                    # Puedes agregar aquí tu código personalizado
                    pass

                return comision
            except Exception as e:
                # Manejo de errores aquí
                return Decimal(0)  # Retornar 0 o algún valor por defecto en caso de error
    def calcular_total(self):
        total = sum(
            servicio_en_orden.calcular_total()
            for servicio_en_orden in self.servicioenorden_set.all()
        )
        return total


class ServicioEnOrden(models.Model):
    orden = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, null=True, blank=True
    )
    cantidad_servicio = models.PositiveIntegerField(default=0, null=True, blank=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True, blank=True
    )
    cantidad_producto = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        unique_together = ["orden", "servicio", "producto"]

    def calcular_total(self):
        total_servicio = 0
        if self.servicio:
            total_servicio = self.servicio.precio * self.cantidad_servicio

        total_producto = 0
        if self.producto:
            total_producto = self.producto.precio * self.cantidad_producto

        return total_servicio + total_producto

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(ServicioEnOrden, self).save(*args, **kwargs)

            # Actualizar la cantidad de productos en el modelo Producto si el producto existe
            if self.producto:
                producto = self.producto
                producto.cantidad -= self.cantidad_producto
                producto.save(update_fields=["cantidad"])
