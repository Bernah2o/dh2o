from django.db import models

class Operador(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=11)
    comisiones = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre, self.apellido)
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Operador, self).save(*args, **kwargs)
        
        

    