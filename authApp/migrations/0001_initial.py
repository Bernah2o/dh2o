# Generated by Django 4.1.1 on 2022-09-30 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('Fecha_nacimiento', models.DateField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.IntegerField()),
                ('correo', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('numerodeservicio', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('numero_factura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(max_length=50)),
                ('cantidad_servicio', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('modo_pago', models.CharField(max_length=50)),
                ('tiempo_servicio', models.DateTimeField()),
                ('descuento', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='authApp.cliente')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operador', to='authApp.operador')),
                ('servicios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicio', to='authApp.servicio')),
            ],
        ),
    ]
