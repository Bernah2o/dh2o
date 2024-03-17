from django.db import models


class Activo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_adquisicion = models.DateField()
    proveedor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.proveedor = self.proveedor.upper()
        super().save(*args, **kwargs)


class InventarioActivo(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.activo} - {self.cantidad} unidades - {self.fecha_registro}"

    def save(self, *args, **kwargs):
        self.ubicacion = self.ubicacion.upper()
        self.responsable = self.responsable.upper()
        super().save(*args, **kwargs)