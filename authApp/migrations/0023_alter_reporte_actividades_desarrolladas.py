# Generated by Django 4.1.1 on 2023-05-23 02:25

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0022_alter_reporte_actividades_desarrolladas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='actividades_desarrolladas',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Act1', 'Inspección y riesgos: Identificar peligros y riesgos en el área.'), ('Act2', 'Cierre de entrada y salida: Verificar cierre para evitar ingreso de agua.'), ('Act3', 'Equipos de protección personal (EPP): Asegurar EPP necesarios.'), ('Act4', 'Bombeo y aspirado: Retirar agua del tanque con equipo.'), ('Act5', 'Limpieza del fondo: Remover sedimentos y residuos del fondo.'), ('Act6', 'Limpieza a presión: Limpiar paredes y techos con alta presión.'), ('Act7', 'Aspirado de residuos: Retirar agua sucia y residuos del tanque.'), ('Act8', 'Inspección final: Verificar limpieza y preparación para desinfección.')], max_length=50),
        ),
    ]
