# Generated by Django 4.1.1 on 2023-05-12 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0016_boya_llavepaso_tanque_tuberia_unionuniversal_valvula_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.inventario')),
            ],
        ),
    ]
