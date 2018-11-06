# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import path

from django.conf import settings
from django.db import models

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received


def unique_file_path(instance, filename):
    base, ext = path.splitext(filename)
    newname = "%s%s" % (instance.usuario.nombre, ext)
    return path.join('comprobantes', newname)


# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=False)
    apellidos = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False, unique=True)
    edad = models.IntegerField(null=False, blank=False)
    empresa = models.CharField(max_length=200, null=True, blank=True)
    puesto = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=False)
    estado = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)
    pago = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return 'Email: {0} y con ID: {1}'.format(self.email, self.id)


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
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Evaluacion # {0} del usuario: {1}'.format(self.id, self.usuario.email)


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
            ('5', 'Analitico'),  # valor = H
            ('6', 'Comprometido'),  # valor = B
            ('7', 'Dinámico'),  # valor = I
            ('8', 'Líder'),  # valor = G
            ('9', 'Conciliador')  # valor = A
        )
    )

    def __str__(self):
        return 'eneatipo: {0}'.format(self.eneatipo)


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
        return 'Centro: {0}'.format(self.centro)


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
        return 'Energia: {0} '.format(self.energia)


class Comprobante(models.Model):
    fecha = models.DateTimeField(null=True, blank=False)
    importe = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    tipo_pago = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('0', 'Taller.'),
            ('1', 'Gratis.'),
            ('2', 'PayPal.'),
            ('3', 'Deposito o Transferencia bancaria.')
        )
    )
    imagen_comprobante = models.ImageField(upload_to=unique_file_path, null=True, blank=True)
    metodo_pago = models.CharField(
        max_length=2, blank=True, default='0', choices=(
            ('0', 'No es deposito a bancos no necesita comprobante.'),
            ('01', 'Efectivo.'),
            ('02', 'Cheque.'),
            ('03', 'Transferencia Electronica.')
        )
    )
    usuario = models.ForeignKey(
        Usuario, null=False, blank=False, related_name='comprobante_user_set', on_delete=models.PROTECT
    )
    evaluacion = models.ForeignKey(
        Evaluacion, null=True, blank=False, related_name='evaluacion_pago_set', on_delete=models.PROTECT
    )

    def __str__(self):
        return 'Comprobante con metodo de pago: {0}'.format(self.get_tipo_pago_display())


class Codigo(models.Model):
    codigo = models.CharField(max_length=200, null=True, blank=False)
    activo = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return 'Codigo: {0}'.format(self.codigo)


def guardar_pago_evaluacion(sender, **kwargs):
    print(sender)
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_BUSINESS:
            return
    else:
        return


valid_ipn_received.connect(guardar_pago_evaluacion)
invalid_ipn_received.connect(guardar_pago_evaluacion)