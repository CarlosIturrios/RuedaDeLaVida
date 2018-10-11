# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.Evaluacion)
admin.site.register(models.Respuesta)
admin.site.register(models.Eneatipo)
admin.site.register(models.Centro)
admin.site.register(models.Energia)
admin.site.register(models.Codigo)
admin.site.register(models.Comprobante)