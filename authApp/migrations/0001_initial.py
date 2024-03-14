# Generated by Django 4.2.1 on 2024-03-14 13:54

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
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_documento', models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('NIT', 'Número de Identificación Tributaria')], default='CC', max_length=3)),
                ('numero_documento', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(blank=True, max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=11, unique=True)),
                ('correo', models.EmailField(blank=True, max_length=100)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('ultima_limpieza', models.DateField(blank=True, null=True)),
                ('proxima_limpieza', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mpago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('numero_cuenta', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=11)),
                ('comisiones', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenDeTrabajo',
            fields=[
                ('numero_orden', models.AutoField(primary_key=True, serialize=False, verbose_name='Número de Orden')),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField()),
                ('facturada', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.cliente')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.operador')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.IntegerField(default=0)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('ordenes_trabajo', models.ManyToManyField(blank=True, to='authApp.ordendetrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ServicioEnOrden',
            fields=[
                ('id_servicio_en_orden', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_servicio', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('cantidad_producto', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_en_orden_detalle', to='authApp.ordendetrabajo')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authApp.producto')),
                ('servicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authApp.servicio')),
            ],
            options={
                'unique_together': {('orden', 'servicio', 'producto')},
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('imagen_antes_lavado_1', models.ImageField(null=True, upload_to='reportes/')),
                ('imagen_antes_lavado_2', models.ImageField(null=True, upload_to='reportes/')),
                ('imagen_despues_lavado_1', models.ImageField(null=True, upload_to='reportes/')),
                ('imagen_despues_lavado_2', models.ImageField(null=True, upload_to='reportes/')),
                ('proxima_limpieza', models.DateField(blank=True, null=True)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('orden_de_trabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.ordendetrabajo')),
                ('servicio_en_orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='authApp.servicioenorden')),
            ],
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='servicios_en_orden',
            field=models.ManyToManyField(blank=True, related_name='ordenes_de_trabajo', through='authApp.ServicioEnOrden', to='authApp.servicio'),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('numero_factura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=10)),
                ('mpago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.mpago')),
                ('orden_de_trabajo', models.ForeignKey(limit_choices_to={'factura__isnull': True}, on_delete=django.db.models.deletion.CASCADE, to='authApp.ordendetrabajo')),
            ],
        ),
    ]
