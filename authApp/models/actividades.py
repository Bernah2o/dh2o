from django.db import models

class Actividad(models.Model):
    id_actividades = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()  # Convierte el nombre a mayúsculas
        super(Actividad, self).save(*args, **kwargs)
