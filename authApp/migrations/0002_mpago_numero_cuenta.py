# Generated by Django 4.2.1 on 2024-03-10 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpago',
            name='numero_cuenta',
            field=models.IntegerField(default=0),
        ),
    ]