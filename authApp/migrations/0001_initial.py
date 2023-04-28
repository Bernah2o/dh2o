# Generated by Django 4.1.1 on 2023-02-27 23:21

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
                ('Fecha_nacimiento', models.DateField(blank=True, max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.IntegerField()),
                ('correo', models.EmailField(blank=True, max_length=100)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Mpago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
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
                ('id_servicio', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('numero_factura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(max_length=50)),
                ('cantidad_servicio', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('tiempo_servicio', models.DurationField()),
                ('descuento', models.IntegerField(blank=True)),
                ('total_servicio', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='authApp.cliente')),
                ('mpago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mpago', to='authApp.mpago')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operador', to='authApp.operador')),
                ('servicios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicio', to='authApp.servicio')),
            ],
        ),
    ]