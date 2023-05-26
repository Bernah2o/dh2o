# Generated by Django 4.1.1 on 2023-05-23 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0025_alter_reporte_imagen_antes_lavado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporte',
            old_name='imagen_antes_lavado',
            new_name='imagen_antes_lavado_1',
        ),
        migrations.RenameField(
            model_name='reporte',
            old_name='imagen_despues_lavado',
            new_name='imagen_antes_lavado_2',
        ),
        migrations.AddField(
            model_name='reporte',
            name='imagen_despues_lavado_1',
            field=models.ImageField(null=True, upload_to='reportes/'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='imagen_despues_lavado_2',
            field=models.ImageField(null=True, upload_to='reportes/'),
        ),
    ]