# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 23:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='respuestas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(db_index=True)),
                ('nivel', models.CharField(choices=[('1', 'Bajo'), ('2', 'Medio'), ('3', 'Alto')], default='1', max_length=1)),
                ('area', models.CharField(choices=[('1', 'Carrera|Empresa'), ('2', 'Finanzas|Dinero'), ('3', 'Salud|Vitalidad'), ('4', 'Familia|Amigos'), ('5', 'Amor|relaciones'), ('6', 'Crecimiento personal|Aprendizaje'), ('7', 'Diversion|Estilo de vida'), ('8', 'Productividad personal')], default='1', max_length=1)),
            ],
        ),
    ]
