# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-01 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eneagrama', '0016_auto_20181024_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='fecha_finalizacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eneatipo',
            name='eneatipo',
            field=models.CharField(choices=[('1', 'Perfeccionista'), ('2', 'Colaborador'), ('3', 'Competitivo'), ('4', 'Creativo'), ('5', 'Analitico'), ('6', 'Comprometido'), ('7', 'Din\xe1mico'), ('8', 'L\xedder'), ('9', 'Conciliador')], max_length=1),
        ),
    ]
