# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=False)
    apellidos = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False, unique=True)
    edad = models.IntegerField(null=False, blank=False)
    empresa = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=False)
    estado = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.CharField(max_length=200, null=True, blank=True)
    pago = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return '{0} con email: {1} y con ID: {2}'.format(self.nombre, self.email, self.id)


class Evaluacion(models.Model):
    usuario = models.ForeignKey(
        Usuario, null=False, blank=False, related_name='evaluacion_user_set', on_delete=models.PROTECT
    )
    # Total de preguntas en numero que se respondieron correspondientes a cada eneatipo.
    tipoUno = models.IntegerField(null=True, blank=False)
    tipoDos = models.IntegerField(null=True, blank=False)
    tipoTres = models.IntegerField(null=True, blank=False)
    tipoCuatro = models.IntegerField(null=True, blank=False)
    tipoCinco = models.IntegerField(null=True, blank=False)
    tipoSeis = models.IntegerField(null=True, blank=False)
    tipoSiete = models.IntegerField(null=True, blank=False)
    tipoOcho = models.IntegerField(null=True, blank=False)
    tipoNueve = models.IntegerField(null=True, blank=False)
    # los 3 principales eneatipos.
    eneatipoPrincipal = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Perfeccionista'),
            ('2', 'Colaborador'),
            ('3', 'Competitivo'),
            ('4', 'Creativo'),
            ('5', 'Analítico'),
            ('6', 'Comprometido'),
            ('7', 'Dinámico'),
            ('8', 'Líder'),
            ('9', 'Conciliador')
        )
    )
    eneatipoSecundario = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Perfeccionista'),
            ('2', 'Colaborador'),
            ('3', 'Competitivo'),
            ('4', 'Creativo'),
            ('5', 'Analítico'),
            ('6', 'Comprometido'),
            ('7', 'Dinámico'),
            ('8', 'Líder'),
            ('9', 'Conciliador')
        )
    )
    eneatipoTerciario = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Perfeccionista'),
            ('2', 'Colaborador'),
            ('3', 'Competitivo'),
            ('4', 'Creativo'),
            ('5', 'Analítico'),
            ('6', 'Comprometido'),
            ('7', 'Dinámico'),
            ('8', 'Líder'),
            ('9', 'Conciliador')
        )
    )
    centroPrimario = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Emocional'),
            ('2', 'Físico'),
            ('3', 'Intelectual')
        )
    )
    centroSecundario = models.CharField(
        max_length=1, blank=False, null=True, choices=(
            ('1', 'Emocional'),
            ('2', 'Físico'),
            ('3', 'Intelectual')
        )
    )
    centroTerciario = models.CharField(
        max_length=1, blank=False, null=True, choices=(
            ('1', 'Emocional'),
            ('2', 'Físico'),
            ('3', 'Intelectual')
        )
    )

    centroEmocional = models.IntegerField(null=True, blank=False)
    centroFisico = models.IntegerField(null=True, blank=False)
    centroIntelectual = models.IntegerField(null=True, blank=False)

    energiaPrimaria = models.CharField(
        max_length=1, blank=False, null=True, choices=(
            ('1', 'Interna'),
            ('2', 'Externa'),
            ('3', 'Equilibrio')
        )
    )
    energiaSecundaria = models.CharField(
        max_length=1, blank=False, null=True, choices=(
            ('1', 'Interna'),
            ('2', 'Externa'),
            ('3', 'Equilibrio')
        )
    )
    energiaTerciaria = models.CharField(
        max_length=1, blank=False, null=True, choices=(
            ('1', 'Interna'),
            ('2', 'Externa'),
            ('3', 'Equilibrio')
        )
    )
    energiaInterna = models.IntegerField(null=True, blank=False)
    energiaExterna = models.IntegerField(null=True, blank=False)
    energiaEquilibrio = models.IntegerField(null=True, blank=False)
    fecha_creacion = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return 'Evaluacion # {0} del usuario: {1}'.format(self.id, self.usuario.nombre)


class Respuesta(models.Model):
    evaluacion = models.ForeignKey(
        Evaluacion, null=True, blank=False, related_name='evaluacion_resuesta_set', on_delete=models.PROTECT
    )
    pregunta = models.CharField(max_length=20, null=False, blank=False)
    valor = models.CharField(max_length=1, null=True, blank=False)

    def __str__(self):
        return '{0} pregunta #{1} con valor: {2}'.format(self.evaluacion, self.pregunta, self.valor)


class Eneatipo(models.Model):
    descripcion = models.TextField(null=True, blank=False)
    eneatipo = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Perfeccionista'),  # valor = D
            ('2', 'Colaborador'),  # valor = F
            ('3', 'Competitivo'),  # valor = C
            ('4', 'Creativo'),  # valor = E
            ('5', 'Analítico'),  # valor = H
            ('6', 'Comprometido'),  # valor = B
            ('7', 'Dinámico'),  # valor = I
            ('8', 'Líder'),  # valor = G
            ('9', 'Conciliador')  # valor = A
        )
    )

    def __str__(self):
        return 'eneatipo: {0}'.format(self.get_eneatipo_display())


class Centro(models.Model):
    descripcion = models.TextField(null=True, blank=False)
    centro = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Emocional'),
            ('2', 'Físico'),
            ('3', 'Intelectual')
        )
    )

    def __str__(self):
        return 'Centro: {0}'.format(self.get_centro_display())


class Energia(models.Model):
    descripcion = models.TextField(null=True, blank=False)
    energia = models.CharField(
        max_length=1, blank=False, choices=(
            ('1', 'Perfeccionista'),  # valor = D
            ('2', 'Colaborador'),  # valor = F
            ('3', 'Competitivo'),  # valor = C
            ('4', 'Creativo'),  # valor = E
            ('5', 'Analítico'),  # valor = H
            ('6', 'Comprometido'),  # valor = B
            ('7', 'Dinámico'),  # valor = I
            ('8', 'Líder'),  # valor = G
            ('9', 'Conciliador')  # valor = A
        )
    )

    def __str__(self):
        return 'Energia: '.format(self.get_energia_display())
