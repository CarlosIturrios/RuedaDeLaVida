# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eneagrama', '0013_auto_20181010_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobante',
            name='importe',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
    ]
