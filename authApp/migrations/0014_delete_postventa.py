# Generated by Django 4.1.1 on 2023-05-01 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0013_remove_postventa_proxima_limpieza_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Postventa',
        ),
    ]