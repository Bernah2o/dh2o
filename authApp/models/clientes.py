from django.db import models


class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True,)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=100, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True)
    ultima_limpieza = models.DateField(null=True, blank=True)
    necesita_limpieza_proximamente = models.BooleanField(default=False)
        
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)
    
    def __str__(self):
        return self.Fecha_nacimiento.strftime('%d/%m/%Y')

    