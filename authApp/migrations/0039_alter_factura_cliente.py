# Generated by Django 4.2.1 on 2023-06-19 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0038_remove_cliente_cedula_cliente_numero_documento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authApp.cliente'),
        ),
    ]