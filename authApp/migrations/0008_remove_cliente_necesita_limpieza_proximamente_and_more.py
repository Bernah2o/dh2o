# Generated by Django 4.1.1 on 2023-04-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0007_repuesto_created_at_alter_repuesto_descripcion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='necesita_limpieza_proximamente',
        ),
        migrations.AddField(
            model_name='cliente',
            name='proxima_limpieza',
            field=models.DateField(blank=True, null=True),
        ),
    ]