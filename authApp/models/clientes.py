from django.db import models

<<<<<<< HEAD
class Cliente(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=100)
    
    def __str__(self) -> str:
        return self.nombre
=======
class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    documento = models.IntegerField()
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateTimeField(max_length=100)
    
>>>>>>> 36107d8ab770179911347914ca535625d306f4d2
