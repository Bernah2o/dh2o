# Generated by Django 4.1.1 on 2023-05-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0006_reporte_proxima_limpieza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_producto',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]