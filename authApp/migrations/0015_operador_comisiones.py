# Generated by Django 4.1.1 on 2023-05-21 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0014_alter_ordendetrabajo_numero_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='operador',
            name='comisiones',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]