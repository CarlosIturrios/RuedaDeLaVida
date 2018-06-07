# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Respuesta(models.Model):
	descripcion = models.TextField(db_index=True, null=False, blank=False)	
	nivel = models.CharField(
		max_length=1, blank=False, default='1', choices=(
			('1','Bajo'),
			('2','Medio'),
			('3','Alto')
		)
	)
	area = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','Carrera|Empresa'),
			('2','Finanzas|Dinero'),
			('3','Salud|Vitalidad'),
			('4','Familia|Amigos'),
			('5','Amor|relaciones'),
			('6','Crecimiento personal|Aprendizaje'),
			('7','Diversion|Estilo de vida'),
			('8','Productividad personal')
		)
	)
	
	def __str__(self):
		return 'id: {0} area: {1} nivel: {2}'.format(self.id, self.get_area_display(), self.get_nivel_display())


class Correo(models.Model):
	nombre = models.CharField(max_length=200, null=False, blank=False)
 	apellidos = models.CharField(max_length=200, null=False, blank=False)
 	correo = models.CharField(max_length=200, null=False, blank=False)

 	def __str__(self):
		return 'Nombre: {0} {1} correo: {2}'.format(self.nombre, self.apellidos, self.correo)