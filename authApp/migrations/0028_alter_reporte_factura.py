# Generated by Django 4.1.1 on 2023-05-26 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0027_reporte_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='factura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authApp.factura'),
        ),
    ]
