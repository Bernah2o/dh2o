# Generated by Django 4.2.1 on 2024-03-12 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0010_alter_servicioenorden_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='servicio_en_orden',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authApp.servicioenorden'),
        ),
    ]