from django.db import models
from django.core.exceptions import ValidationError
from authApp.models.factura import Factura


class OrdenDeTrabajo(models.Model):
    numero_orden = models.AutoField(primary_key=True, verbose_name="Número de Orden")
    fecha = models.DateField()
    cliente = models.ForeignKey("authApp.Cliente", on_delete=models.CASCADE)
    servicios = models.ManyToManyField("authApp.Servicio")
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
            # Obtener la suma total de los precios de todos los servicios
            total_servicios = sum(servicio.precio for servicio in self.servicios.all())

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
        # Utilizar diccionarios para realizar el seguimiento de la cantidad y el precio de cada servicio y producto
        cantidad_servicios = {}
        precio_servicios = {}

        cantidad_productos = {}
        precio_productos = {}

        # Calcular la cantidad y el precio de cada servicio en la orden de trabajo
        for servicio in self.servicios.all():
            if servicio in cantidad_servicios:
                cantidad_servicios[servicio] += 1
            else:
                cantidad_servicios[servicio] = 1
                precio_servicios[servicio] = servicio.precio

        # Calcular la cantidad y el precio de cada producto en la orden de trabajo
        for producto in self.productos.all():
            if producto in cantidad_productos:
                cantidad_productos[producto] += 1
            else:
                cantidad_productos[producto] = 1
                precio_productos[producto] = producto.precio

        # Calcular el total sumando el precio de cada servicio y producto multiplicado por su cantidad
        total = 0

        for servicio, cantidad in cantidad_servicios.items():
            total += precio_servicios[servicio] * cantidad

        for producto, cantidad in cantidad_productos.items():
            total += precio_productos[producto] * cantidad

        return total
