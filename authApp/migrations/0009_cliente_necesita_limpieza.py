# Generated by Django 4.1.1 on 2023-04-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0008_remove_cliente_necesita_limpieza_proximamente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='necesita_limpieza',
            field=models.BooleanField(default=False),
        ),
    ]
