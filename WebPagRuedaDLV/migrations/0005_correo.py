# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebPagRuedaDLV', '0004_auto_20180604_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellidos', models.CharField(max_length=200)),
                ('correo', models.CharField(max_length=200)),
            ],
        ),
    ]
