# Generated by Django 4.1.1 on 2023-04-29 21:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0011_postventa'),
    ]

    operations = [
        migrations.AddField(
            model_name='postventa',
            name='comentario',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='postventa',
            name='fecha',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postventa',
            name='proxima_limpieza',
            field=models.DateField(blank=True, null=True),
        ),
    ]
