from django.db import models

class Tanque(models.Model):
    modelo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    material = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"Tanque {self.modelo}"