# Generated by Django 4.2.1 on 2024-04-25 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0008_delete_cuentabancaria_operador_banco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operador',
            name='comisiones',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]