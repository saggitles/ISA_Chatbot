# Generated by Django 2.1.5 on 2021-10-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isa', '0008_auto_20211008_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensajeMasivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(blank=True, max_length=255, null=True)),
                ('mensaje', models.TextField(blank=True, null=True)),
                ('ultimaModificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
