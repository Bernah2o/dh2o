# Generated by Django 4.1.1 on 2023-05-16 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0003_alter_reporte_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='proxima_limpieza',
        ),
    ]
