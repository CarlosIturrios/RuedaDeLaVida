# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-01 03:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eneagrama', '0002_auto_20180831_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='evaluacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluacion_resuesta_set', to='Eneagrama.Evaluacion'),
        ),
    ]