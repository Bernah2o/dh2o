# Generated by Django 4.1.1 on 2023-05-10 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0009_ordendetrabajo_numero_orden'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='Fecha_nacimiento',
            new_name='fecha_nacimiento',
        ),
    ]
