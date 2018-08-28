# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=False)
    apellidos = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    empresa = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=False)
    ciudad = models.CharField(max_length=200, null=True, blank=True)