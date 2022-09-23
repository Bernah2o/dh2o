from django.db import models

<<<<<<< HEAD
class Servicio(models.Model):
    numerodeservicio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.numerodeservicio
=======
class Servicios(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200)
    precio = models.IntegerField()
>>>>>>> 36107d8ab770179911347914ca535625d306f4d2
