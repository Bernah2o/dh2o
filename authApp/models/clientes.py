from django.db import models
from datetime import date, timedelta, timezone
from authApp.models.servicios import Servicio

class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=11)
    correo = models.EmailField(max_length=100, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True) 
    ultima_limpieza = models.DateField(null=True, blank=True) # Fecha de última limpieza
    proxima_limpieza = models.DateField(null=True, blank=True) # Fecha de próxima limpieza
    servicios = models.ManyToManyField(Servicio) # Relación con el modelo Servicio
          
           
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper() # Convertir el nombre a mayúsculas antes de guardar
        self.apellido = self.apellido.upper() # Convertir el apellido a mayúsculas antes de guardar
        self.direccion = self.direccion.upper() # Convertir la dirección a mayúsculas antes de guardar
        if self.ultima_limpieza:
            # Calcular fecha de próxima limpieza
            frecuencia_meses = 6 # Frecuencia de limpieza en meses, cambiar según necesidades
            delta_meses = timedelta(days=30*int(frecuencia_meses)) # Duración en días de la frecuencia de limpieza
            self.proxima_limpieza = self.ultima_limpieza + delta_meses # Calcular la fecha de próxima limpieza
        super().save(*args, **kwargs)

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)
    
    def proximas_limpiezas(self):
        """Retorna una lista de clientes que tienen próxima limpieza"""
        hoy = timezone.now().date() # Fecha actual
        proximos = [] # Lista de clientes con próxima limpieza
        for cliente in Cliente.objects.all(): # Iterar sobre todos los clientes
            if cliente.proxima_limpieza and cliente.proxima_limpieza <= hoy:
                proximos.append(cliente) # Agregar el cliente a la lista si su próxima limpieza es anterior o igual a la fecha actual
        return proximos
        
    
    

