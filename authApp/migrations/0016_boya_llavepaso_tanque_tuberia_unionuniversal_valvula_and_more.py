# Generated by Django 4.1.1 on 2023-05-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0015_rename_marca_tanque_inventario_tanque_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LlavePaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diametro', models.CharField(max_length=3)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100)),
                ('capacidad', models.CharField(choices=[('1000', 'Tanque de 1000 litros'), ('2000', 'Tanque de 2000 litros'), ('5000', 'Tanque de 5000 litros')], max_length=4)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tuberia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitud', models.DecimalField(decimal_places=2, max_digits=5)),
                ('diametro', models.CharField(choices=[('1/2', '1/2 pulgada'), ('3/4', '3/4 pulgada'), ('1', '1 pulgada')], max_length=3)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UnionUniversal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diametro', models.CharField(max_length=3)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Valvula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diametro', models.CharField(max_length=3)),
                ('tipo', models.CharField(choices=[('Compuerta', 'Compuerta'), ('Mariposa', 'Mariposa'), ('Check', 'Check')], max_length=20)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ValvulaCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diametro', models.CharField(max_length=3)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='boya',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='llave_paso',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='tanque',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='union_universal',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='valvula_check',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='tuberias',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='valvulas',
        ),
        migrations.AddField(
            model_name='inventario',
            name='boyas',
            field=models.ManyToManyField(to='authApp.boya'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='llaves_paso',
            field=models.ManyToManyField(to='authApp.llavepaso'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='tanques',
            field=models.ManyToManyField(to='authApp.tanque'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='uniones_universales',
            field=models.ManyToManyField(to='authApp.unionuniversal'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='valvulas_check',
            field=models.ManyToManyField(to='authApp.valvulacheck'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='tuberias',
            field=models.ManyToManyField(to='authApp.tuberia'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='valvulas',
            field=models.ManyToManyField(to='authApp.valvula'),
        ),
    ]
