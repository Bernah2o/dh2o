from django.db import models
from django.core.exceptions import ValidationError
from authApp.models.factura import Factura
from authApp.models.servicios import Servicio


class OrdenDeTrabajo(models.Model):
    numero_orden = models.AutoField(primary_key=True, verbose_name="Número de Orden")
    fecha = models.DateField()
    cliente = models.ForeignKey("authApp.Cliente", on_delete=models.CASCADE)
    operador = models.ForeignKey("authApp.Operador", on_delete=models.CASCADE)
    descripcion = models.TextField()
    productos = models.ManyToManyField("authApp.Producto", blank=True)
    facturada = models.BooleanField(default=False)

    def __str__(self):
        return f"OrdenDeTrabajo {self.numero_orden}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto no tiene clave primaria asignada (es nuevo)
            ultima_orden = OrdenDeTrabajo.objects.order_by("-numero_orden").first()
            if ultima_orden:
                self.numero_orden = ultima_orden.numero_orden + 1
            else:
                self.numero_orden = 1

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
            total_servicios = sum(servicio_en_orden.servicio.precio * servicio_en_orden.cantidad 
                                for servicio_en_orden in self.servicios_en_orden.all())

            # Calcular la comisión como el 10% de la suma total de servicios
            comision = total_servicios * 0.1

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
            print("Error al calcular la comisión:", e)
            return 0  # Retornar 0 o algún valor por defecto en caso de error


    def calcular_total(self):
        total = 0
        for servicio_en_orden in self.servicios_en_orden.all():
            total += servicio_en_orden.calcular_total()
        return total


class ServicioEnOrden(models.Model):
    orden_de_trabajo = models.ForeignKey(
        "OrdenDeTrabajo", on_delete=models.CASCADE, related_name="servicios_en_orden"
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ["orden_de_trabajo", "servicio"]

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto no tiene clave primaria asignada (es nuevo)
            ultima_orden = OrdenDeTrabajo.objects.order_by("-numero_orden").first()
            if ultima_orden:
                self.numero_orden = ultima_orden.numero_orden + 1
            else:
                self.numero_orden = 1

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk:
            existing_facturas = Factura.objects.filter(orden_de_trabajo=self)
            if existing_facturas.exists():
                raise ValidationError(
                    "Esta orden de trabajo ya tiene una factura asociada."
                )

    def calcular_total(self):
        return self.servicio.precio * self.cantidad
