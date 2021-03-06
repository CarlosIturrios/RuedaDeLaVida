# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-03 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eneagrama', '0010_auto_20180903_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='centroSecundario',
            field=models.CharField(choices=[('1', 'Emocional'), ('2', 'F\xedsico'), ('3', 'Intelectual')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='centroTerciario',
            field=models.CharField(choices=[('1', 'Emocional'), ('2', 'F\xedsico'), ('3', 'Intelectual')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='energiaPrimaria',
            field=models.CharField(choices=[('1', 'Interna'), ('2', 'Externa'), ('3', 'Equilibrio')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='energiaSecundaria',
            field=models.CharField(choices=[('1', 'Interna'), ('2', 'Externa'), ('3', 'Equilibrio')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='energiaTerciaria',
            field=models.CharField(choices=[('1', 'Interna'), ('2', 'Externa'), ('3', 'Equilibrio')], max_length=1, null=True),
        ),
    ]
