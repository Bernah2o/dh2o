# Generated by Django 4.1.1 on 2023-05-20 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0012_factura_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='orden_de_trabajo',
            field=models.ForeignKey(limit_choices_to={'factura__isnull': True}, on_delete=django.db.models.deletion.CASCADE, to='authApp.ordendetrabajo'),
        ),
    ]