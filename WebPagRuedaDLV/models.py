# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=200, null=True, blank=False)
    posicion = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'primera'),
            ('2', 'segunda'),
        )
    )
    area = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Carrera|Empresa'),
            ('2', 'Finanzas|Dinero'),
            ('3', 'Salud|Vitalidad'),
            ('4', 'Familia|Amigos'),
            ('5', 'Amor|relaciones'),
            ('6', 'Crecimiento personal|Aprendizaje'),
            ('7', 'Diversion|Estilo de vida'),
            ('8', 'Productividad personal')
        )
    )

    def __str__(self):
        return 'pregunta: {0} area: {1} posicion: {2} id: {3}'.format(self.pregunta, self.get_area_display(), self.get_posicion_display(), self.id)


class Respuesta(models.Model):
    descripcion = models.TextField(null=False, blank=False)
    nivel = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Bajo'),
            ('2', 'Medio'),
            ('3', 'Alto')
        )
    )
    area = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Carrera|Empresa'),
            ('2', 'Finanzas|Dinero'),
            ('3', 'Salud|Vitalidad'),
            ('4', 'Familia|Amigos'),
            ('5', 'Amor|relaciones'),
            ('6', 'Crecimiento personal|Aprendizaje'),
            ('7', 'Diversion|Estilo de vida'),
            ('8', 'Productividad personal')
        )
    )

    def __str__(self):
        return 'id: {0} area: {1} nivel: {2}'.format(self.id, self.get_area_display(), self.get_nivel_display())


class Correo(models.Model):
    usuario = models.CharField(max_length=200, null=True, blank=False)
    apellidos = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    slide1 = models.CharField(max_length=200, null=True, blank=False)
    slide2 = models.CharField(max_length=200, null=True, blank=False)
    text1 = models.CharField(max_length=200, null=True, blank=False)
    text2 = models.CharField(max_length=200, null=True, blank=False)
    carrera = models.CharField(max_length=200, null=True, blank=False)
    slide3 = models.CharField(max_length=200, null=True, blank=False)
    slide4 = models.CharField(max_length=200, null=True, blank=False)
    text3 = models.CharField(max_length=200, null=True, blank=False)
    text4 = models.CharField(max_length=200, null=True, blank=False)
    finanzas = models.CharField(max_length=200, null=True, blank=False)
    slide5 = models.CharField(max_length=200, null=True, blank=False)
    slide6 = models.CharField(max_length=200, null=True, blank=False)
    text5 = models.CharField(max_length=200, null=True, blank=False)
    text6 = models.CharField(max_length=200, null=True, blank=False)
    salud = models.CharField(max_length=200, null=True, blank=False)
    slide7 = models.CharField(max_length=200, null=True, blank=False)
    slide8 = models.CharField(max_length=200, null=True, blank=False)
    text7 = models.CharField(max_length=200, null=True, blank=False)
    text8 = models.CharField(max_length=200, null=True, blank=False)
    familia = models.CharField(max_length=200, null=True, blank=False)
    slide9 = models.CharField(max_length=200, null=True, blank=False)
    slide10 = models.CharField(max_length=200, null=True, blank=False)
    text9 = models.CharField(max_length=200, null=True, blank=False)
    text10 = models.CharField(max_length=200, null=True, blank=False)
    amor = models.CharField(max_length=200, null=True, blank=False)
    slide11 = models.CharField(max_length=200, null=True, blank=False)
    slide12 = models.CharField(max_length=200, null=True, blank=False)
    text11 = models.CharField(max_length=200, null=True, blank=False)
    text12 = models.CharField(max_length=200, null=True, blank=False)
    crecimiento = models.CharField(max_length=200, null=True, blank=False)
    slide13 = models.CharField(max_length=200, null=True, blank=False)
    slide14 = models.CharField(max_length=200, null=True, blank=False)
    text13 = models.CharField(max_length=200, null=True, blank=False)
    text14 = models.CharField(max_length=200, null=True, blank=False)
    diversion = models.CharField(max_length=200, null=True, blank=False)
    slide15 = models.CharField(max_length=200, null=True, blank=False)
    slide16 = models.CharField(max_length=200, null=True, blank=False)
    text15 = models.CharField(max_length=200, null=True, blank=False)
    text16 = models.CharField(max_length=200, null=True, blank=False)
    productividad = models.CharField(max_length=200, null=True, blank=False)
    gaptotal = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return 'Nombre: {0} {1} correo: {2}'.format(self.usuario, self.apellidos, self.email)
