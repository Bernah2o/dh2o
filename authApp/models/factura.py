from django.db import models

class Factura(models.Model):
    fecha = models.DateField(max_length=50)

    