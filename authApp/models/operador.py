from django.db import models


class Operador(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="operador_fotos", null=True, blank=True)
    telefono = models.CharField(max_length=11)
    comisiones = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    banco = models.CharField(max_length=100, null=True, blank=True)
    numero_cuenta = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.banco = self.banco.upper()
        super(Operador, self).save(*args, **kwargs)
