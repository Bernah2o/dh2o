from django.db import models

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.nombre} - {self.get_precio()}"
    def get_precio(self):
        return f"${format(self.precio, ',.0f')}"
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper() # Convertir el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs) # Llamar al método save de la clase padre para guardar los datos
    