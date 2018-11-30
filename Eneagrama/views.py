# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PIL.Image import eval

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse  # email sender
from django.template import Context  # email sender
from django.template.loader import render_to_string, get_template  # email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives  # email sender
from django.core import signing
from django.conf import settings
from django.views.generic import View, TemplateView
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from datetime import date, datetime
from io import BytesIO
from reportlab.pdfgen import canvas, textobject
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.spider import SpiderChart
from paypal.standard.forms import PayPalPaymentsForm

from reportlab.platypus import Paragraph, Table, TableStyle, Image

from .models import Usuario, Evaluacion, Respuesta, Energia, Centro, Eneatipo, Codigo, Comprobante


def principal(request):
    if request.user.is_authenticated():
        return redirect('Eneagrama:Dashboard')
    return render(request, 'eneagrama/principal.html')


def register(request, metodo_pago):
    metodoPago = metodo_pago
    request.session['metodoPago'] = metodoPago
    if 'nombre' in request.session:
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        messages.success(request, '¡Bienvenido de nuevo {0} {1}!'.format(evaluacion.usuario.nombre,
                                                                         evaluacion.usuario.apellidos))
        comprobante = Comprobante.objects.filter(usuario=evaluacion.usuario).first()
        if comprobante:
            if comprobante.tipo_pago == '0':
                return redirect('Eneagrama:parteUno')
            elif comprobante.tipo_pago == '1':
                return redirect('Eneagrama:parteUno')
            else:
                if evaluacion.usuario.pago == True:
                    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
                    if preguntas < 144:
                        return redirect('Eneagrama:parteUno')
                    else:
                        return redirect('Eneagrama:pago_formato')
                else:
                    return redirect('Eneagrama:realizar_pago')
        else:
            return redirect('Eneagrama:realizar_pago')
    nombreMostrar = None
    codigos = Codigo.objects.filter(activo=True)
    if request.method == "POST":
        metPago = request.POST.get('metodoPago', None)
        if metPago:
            metodoPago = metPago
            request.session['metodoPago'] = metodoPago
    if metodoPago == '0':
        if request.method == "POST":
            nombre = request.POST.get('nombre', None)
            apellidos = request.POST.get('apellidos', None)
            email = request.POST.get('email', None)
            edad = request.POST.get('edad', None)
            empresa = request.POST.get('empresa', None)
            puesto = request.POST.get('puesto', None)
            pais = request.POST.get('pais', None)
            estado = request.POST.get('estado', None)
            ciudad = request.POST.get('ciudad', None)
            codigo = request.POST.get('codigo', None)
            check_email = Usuario.objects.filter(email=email).first()
            if check_email:
                request.session['id_user'] = check_email.id
                check_email.nombre = nombre
                check_email.apellidos = apellidos
                check_email.email = email
                check_email.edad = edad
                check_email.empresa = empresa
                check_email.puesto = puesto
                check_email.pais = pais
                check_email.estado = estado
                check_email.ciudad = ciudad
                check_email.codigo = codigo
                check_email.pago = True
                check_email.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion.objects.filter(usuario=check_email).last()
                if evaluacion:
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                else:
                    evaluacion = Evaluacion()
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                comprobante = Comprobante.objects.filter(usuario=check_email).last()
                if comprobante:
                    comprobante.tipo_pago = '0'
                    comprobante.usuario = check_email
                    comprobante.evaluacion = evaluacion
                    comprobante.save()
                else:
                    comprobante = Comprobante()
                    comprobante.tipo_pago = '0'
                    comprobante.usuario = check_email
                    comprobante.evaluacion = evaluacion
                    comprobante.save()
                messages.success(request, '¡Bienvenido {0} {1}'.format(check_email.nombre, check_email.apellidos))
                return redirect('Eneagrama:parteUno')
            else:
                usuario = Usuario()
                usuario.nombre = nombre
                usuario.apellidos = apellidos
                usuario.email = email
                usuario.edad = edad
                usuario.empresa = empresa
                usuario.puesto = puesto
                usuario.pais = pais
                usuario.estado = estado
                usuario.ciudad = ciudad
                usuario.codigo = codigo
                usuario.pago = True
                usuario.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion()
                evaluacion.usuario = usuario
                evaluacion.save()
                comprobante = Comprobante()
                comprobante.tipo_pago = '0'
                comprobante.usuario = usuario
                comprobante.evaluacion = evaluacion
                comprobante.save()
                request.session['id_evaluacion'] = evaluacion.id
                return redirect('Eneagrama:parteUno')
    elif metodoPago == '1':
        if request.method == "POST":
            nombre = request.POST.get('nombre', None)
            apellidos = request.POST.get('apellidos', None)
            email = request.POST.get('email', None)
            edad = request.POST.get('edad', None)
            empresa = request.POST.get('empresa', None)
            puesto = request.POST.get('puesto', None)
            pais = request.POST.get('pais', None)
            estado = request.POST.get('estado', None)
            ciudad = request.POST.get('ciudad', None)
            check_email = Usuario.objects.filter(email=email).first()
            if check_email:
                request.session['id_user'] = check_email.id
                check_email.nombre = nombre
                check_email.apellidos = apellidos
                check_email.email = email
                check_email.edad = edad
                check_email.empresa = empresa
                check_email.puesto = puesto
                check_email.pais = pais
                check_email.estado = estado
                check_email.ciudad = ciudad
                check_email.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion.objects.filter(usuario=check_email).last()
                if evaluacion:
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                else:
                    evaluacion = Evaluacion()
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                comprobante = Comprobante.objects.filter(usuario=check_email).last()
                if comprobante:
                    comprobante.tipo_pago = '1'
                    comprobante.usuario = check_email
                    comprobante.evaluacion = evaluacion
                    comprobante.save()
                else:
                    comprobante = Comprobante()
                    comprobante.tipo_pago = '1'
                    comprobante.usuario = check_email
                    comprobante.evaluacion = evaluacion
                    comprobante.save()
                messages.success(request, '¡Bienvenido {0} {1}'.format(check_email.nombre, check_email.apellidos))
                return redirect('Eneagrama:parteUno')
            else:
                usuario = Usuario()
                usuario.nombre = nombre
                usuario.apellidos = apellidos
                usuario.email = email
                usuario.edad = edad
                usuario.empresa = empresa
                usuario.puesto = puesto
                usuario.pais = pais
                usuario.estado = estado
                usuario.ciudad = ciudad
                usuario.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion()
                evaluacion.usuario = usuario
                evaluacion.save()
                comprobante = Comprobante()
                comprobante.tipo_pago = '1'
                comprobante.usuario = usuario
                comprobante.evaluacion = evaluacion
                comprobante.save()
                request.session['id_evaluacion'] = evaluacion.id
                return redirect('Eneagrama:parteUno')
    elif metodoPago == '2':
        if request.method == "POST":
            nombre = request.POST.get('nombre', None)
            apellidos = request.POST.get('apellidos', None)
            email = request.POST.get('email', None)
            edad = request.POST.get('edad', None)
            empresa = request.POST.get('empresa', None)
            puesto = request.POST.get('puesto', None)
            pais = request.POST.get('pais', None)
            estado = request.POST.get('estado', None)
            ciudad = request.POST.get('ciudad', None)
            check_email = Usuario.objects.filter(email=email).first()
            if check_email:
                request.session['id_user'] = check_email.id
                check_email.nombre = nombre
                check_email.apellidos = apellidos
                check_email.email = email
                check_email.edad = edad
                check_email.empresa = empresa
                check_email.puesto = puesto
                check_email.pais = pais
                check_email.estado = estado
                check_email.ciudad = ciudad
                check_email.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion.objects.filter(usuario=check_email).last()
                if evaluacion:
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                else:
                    evaluacion = Evaluacion()
                    evaluacion.usuario = check_email
                    evaluacion.save()
                    request.session['id_evaluacion'] = evaluacion.id
                messages.success(request, '¡Bienvenido {0} {1}'.format(check_email.nombre, check_email.apellidos))
                return redirect('Eneagrama:realizar_pago')
            else:
                usuario = Usuario()
                usuario.nombre = nombre
                usuario.apellidos = apellidos
                usuario.email = email
                usuario.edad = edad
                usuario.empresa = empresa
                usuario.puesto = puesto
                usuario.pais = pais
                usuario.estado = estado
                usuario.ciudad = ciudad
                usuario.save()
                request.session['nombre'] = nombre
                evaluacion = Evaluacion()
                evaluacion.usuario = usuario
                evaluacion.save()
                request.session['id_evaluacion'] = evaluacion.id
                return redirect('Eneagrama:realizar_pago')

    return render(request, 'eneagrama/register.html',
                  {'nombreMostrar': nombreMostrar, 'metodoPago': metodoPago, 'codigos': codigos})


def parteUno(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='1').first()
    pregunta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='2').first()
    pregunta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='3').first()
    pregunta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='4').first()
    pregunta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='5').first()
    pregunta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='6').first()
    pregunta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='7').first()
    pregunta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='8').first()
    pregunta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='9').first()
    pregunta_diez = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='10').first()
    pregunta_once = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='11').first()
    pregunta_doce = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='12').first()
    pregunta_trese = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='13').first()
    pregunta_catorce = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='14').first()
    pregunta_quince = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='15').first()
    pregunta_diesiseis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='16').first()
    pregunta_diesisiete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='17').first()
    pregunta_diesiocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='18').first()
    pregunta_diesinueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='19').first()
    pregunta_veinte = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='20').first()
    if request.method == "POST":
        preguntaUno = request.POST.get('preguntaUno', None)
        preguntaDos = request.POST.get('preguntaDos', None)
        preguntaTres = request.POST.get('preguntaTres', None)
        preguntaCuatro = request.POST.get('preguntaCuatro', None)
        preguntaCinco = request.POST.get('preguntaCinco', None)
        preguntaSeis = request.POST.get('preguntaSeis', None)
        preguntaSiete = request.POST.get('preguntaSiete', None)
        preguntaOcho = request.POST.get('preguntaOcho', None)
        preguntaNueve = request.POST.get('preguntaNueve', None)
        preguntaDiez = request.POST.get('preguntaDiez', None)
        preguntaOnce = request.POST.get('preguntaOnce', None)
        preguntaDoce = request.POST.get('preguntaDoce', None)
        preguntaTrece = request.POST.get('preguntaTrece', None)
        preguntaCatorce = request.POST.get('preguntaCatorce', None)
        preguntaQuince = request.POST.get('preguntaQuince', None)
        preguntaDieciseis = request.POST.get('preguntaDieciseis', None)
        preguntaDiecisiete = request.POST.get('preguntaDiecisiete', None)
        preguntaDieciocho = request.POST.get('preguntaDieciocho', None)
        preguntaDiecinueve = request.POST.get('preguntaDiecinueve', None)
        preguntaVeinte = request.POST.get('preguntaVeinte', None)
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='1')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='2')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='3')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='4')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='5')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='6')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='7')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='8')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='9')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='10')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiez
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='11')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOnce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='12')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDoce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='13')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTrece
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='14')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCatorce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='15')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaQuince
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='16')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDieciseis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='17')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiecisiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='18')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDieciocho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='19')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiecinueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='20')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeinte
        respuesta.save()
        return redirect('Eneagrama:parteDos')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_1.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_uno': pregunta_uno,
                                                                             'pregunta_dos': pregunta_dos,
                                                                             'pregunta_tres': pregunta_tres,
                                                                             'pregunta_cuatro': pregunta_cuatro,
                                                                             'pregunta_cinco': pregunta_cinco,
                                                                             'pregunta_seis': pregunta_seis,
                                                                             'pregunta_siete': pregunta_siete,
                                                                             'pregunta_ocho': pregunta_ocho,
                                                                             'pregunta_nueve': pregunta_nueve,
                                                                             'pregunta_diez': pregunta_diez,
                                                                             'pregunta_once': pregunta_once,
                                                                             'pregunta_doce': pregunta_doce,
                                                                             'pregunta_trese': pregunta_trese,
                                                                             'pregunta_catorce': pregunta_catorce,
                                                                             'pregunta_quince': pregunta_quince,
                                                                             'pregunta_diesiseis': pregunta_diesiseis,
                                                                             'pregunta_diesisiete': pregunta_diesisiete,
                                                                             'pregunta_diesiocho': pregunta_diesiocho,
                                                                             'pregunta_diesinueve': pregunta_diesinueve,
                                                                             'pregunta_veinte': pregunta_veinte})


def parteDos(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_veinti_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='21').first()
    pregunta_veinti_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='22').first()
    pregunta_veinti_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='23').first()
    pregunta_veinti_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='24').first()
    pregunta_veinti_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='25').first()
    pregunta_veinti_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='26').first()
    pregunta_veinti_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='27').first()
    pregunta_veinti_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='28').first()
    pregunta_veinti_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='29').first()
    pregunta_treinta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='30').first()
    pregunta_treinta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='31').first()
    pregunta_treinta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='32').first()
    pregunta_treinta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='33').first()
    pregunta_treinta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='34').first()
    pregunta_treinta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='35').first()
    pregunta_treinta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='36').first()
    pregunta_treinta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='37').first()
    pregunta_treinta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='38').first()
    pregunta_treinta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='39').first()
    pregunta_cuarenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='40').first()

    if request.method == "POST":
        preguntaVeintiUno = request.POST.get('preguntaVeintiUno', None)
        preguntaVeintiDos = request.POST.get('preguntaVeintiDos', None)
        preguntaVeintiTres = request.POST.get('preguntaVeintiTres', None)
        preguntaVeintiCuatro = request.POST.get('preguntaVeintiCuatro', None)
        preguntaVeintiCinco = request.POST.get('preguntaVeintiCinco', None)
        preguntaVeintiSeis = request.POST.get('preguntaVeintiSeis', None)
        preguntaVeintiSiete = request.POST.get('preguntaVeintiSiete', None)
        preguntaVeintiOcho = request.POST.get('preguntaVeintiOcho', None)
        preguntaVeintiNueve = request.POST.get('preguntaVeintiNueve', None)
        preguntaTreinta = request.POST.get('preguntaTreinta', None)
        preguntaTreintayUno = request.POST.get('preguntaTreintayUno', None)
        preguntaTreintayDos = request.POST.get('preguntaTreintayDos', None)
        preguntaTreintayTres = request.POST.get('preguntaTreintayTres', None)
        preguntaTreintayCuatro = request.POST.get('preguntaTreintayCuatro', None)
        preguntaTreintayCinco = request.POST.get('preguntaTreintayCinco', None)
        preguntaTreintaySeis = request.POST.get('preguntaTreintaySeis', None)
        preguntaTreintaySiete = request.POST.get('preguntaTreintaySiete', None)
        preguntaTreintayOcho = request.POST.get('preguntaTreintayOcho', None)
        preguntaTreintayNueve = request.POST.get('preguntaTreintayNueve', None)
        preguntaCuarenta = request.POST.get('preguntaCuarenta', None)
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='21')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='22')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='23')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='24')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='25')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='26')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='27')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='28')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='29')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='30')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreinta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='31')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='32')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='33')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='34')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='35')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='36')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='37')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='38')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='39')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='40')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarenta
        respuesta.save()
        return redirect('Eneagrama:parteTres')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_2.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_veinti_uno': pregunta_veinti_uno,
                                                                             'pregunta_veinti_dos': pregunta_veinti_dos,
                                                                             'pregunta_veinti_tres': pregunta_veinti_tres,
                                                                             'pregunta_veinti_cuatro': pregunta_veinti_cuatro,
                                                                             'pregunta_veinti_cinco': pregunta_veinti_cinco,
                                                                             'pregunta_veinti_seis': pregunta_veinti_seis,
                                                                             'pregunta_veinti_siete': pregunta_veinti_siete,
                                                                             'pregunta_veinti_ocho': pregunta_veinti_ocho,
                                                                             'pregunta_veinti_nueve': pregunta_veinti_nueve,
                                                                             'pregunta_treinta': pregunta_treinta,
                                                                             'pregunta_treinta_uno': pregunta_treinta_uno,
                                                                             'pregunta_treinta_dos': pregunta_treinta_dos,
                                                                             'pregunta_treinta_tres': pregunta_treinta_tres,
                                                                             'pregunta_treinta_cuatro': pregunta_treinta_cuatro,
                                                                             'pregunta_treinta_cinco': pregunta_treinta_cinco,
                                                                             'pregunta_treinta_seis': pregunta_treinta_seis,
                                                                             'pregunta_treinta_siete': pregunta_treinta_siete,
                                                                             'pregunta_treinta_ocho': pregunta_treinta_ocho,
                                                                             'pregunta_treinta_nueve': pregunta_treinta_nueve,
                                                                             'pregunta_cuarenta': pregunta_cuarenta})


def parteTres(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_cuarenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='41').first()
    pregunta_cuarenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='42').first()
    pregunta_cuarenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='43').first()
    pregunta_cuarenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='44').first()
    pregunta_cuarenta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='45').first()
    pregunta_cuarenta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='46').first()
    pregunta_cuarenta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='47').first()
    pregunta_cuarenta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='48').first()
    pregunta_cuarenta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='49').first()
    pregunta_cincuenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='50').first()
    pregunta_cincuenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='51').first()
    pregunta_cincuenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='52').first()
    pregunta_cincuenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='53').first()
    pregunta_cincuenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='54').first()
    pregunta_cincuenta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='55').first()
    pregunta_cincuenta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='56').first()
    pregunta_cincuenta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='57').first()
    pregunta_cincuenta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='58').first()
    pregunta_cincuenta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='59').first()
    pregunta_sesenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='60').first()
    if request.method == "POST":
        preguntaCuarentayUno = request.POST.get('preguntaCuarentayUno', None)
        preguntaCuarentayDos = request.POST.get('preguntaCuarentayDos', None)
        preguntaCuarentayTres = request.POST.get('preguntaCuarentayTres', None)
        preguntaCuarentayCuatro = request.POST.get('preguntaCuarentayCuatro', None)
        preguntaCuarentayCinco = request.POST.get('preguntaCuarentayCinco', None)
        preguntaCuarentaySeis = request.POST.get('preguntaCuarentaySeis', None)
        preguntaCuarentaySiete = request.POST.get('preguntaCuarentaySiete', None)
        preguntaCuarentayOcho = request.POST.get('preguntaCuarentayOcho', None)
        preguntaCuarentayNueve = request.POST.get('preguntaCuarentayNueve', None)
        preguntaCincuenta = request.POST.get('preguntaCincuenta', None)
        preguntaCincuentayUno = request.POST.get('preguntaCincuentayUno', None)
        preguntaCincuentayDos = request.POST.get('preguntaCincuentayDos', None)
        preguntaCincuentayTres = request.POST.get('preguntaCincuentayTres', None)
        preguntaCincuentayCuatro = request.POST.get('preguntaCincuentayCuatro', None)
        preguntaCincuentayCinco = request.POST.get('preguntaCincuentayCinco', None)
        preguntaCincuentaySeis = request.POST.get('preguntaCincuentaySeis', None)
        preguntaCincuentaySiete = request.POST.get('preguntaCincuentaySiete', None)
        preguntaCincuentayOcho = request.POST.get('preguntaCincuentayOcho', None)
        preguntaCincuentayNueve = request.POST.get('preguntaCincuentayNueve', None)
        preguntaSesenta = request.POST.get('preguntaSesenta', None)
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='41')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='42')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='43')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='44')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='45')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='46')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='47')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='48')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='49')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='50')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='51')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='52')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='53')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='54')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='55')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='56')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='57')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='58')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='59')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='60')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesenta
        respuesta.save()
        return redirect('Eneagrama:parteCuatro')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_3.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_cuarenta_uno': pregunta_cuarenta_uno,
                                                                             'pregunta_cuarenta_dos': pregunta_cuarenta_dos,
                                                                             'pregunta_cuarenta_tres': pregunta_cuarenta_tres,
                                                                             'pregunta_cuarenta_cuatro': pregunta_cuarenta_cuatro,
                                                                             'pregunta_cuarenta_cinco': pregunta_cuarenta_cinco,
                                                                             'pregunta_cuarenta_seis': pregunta_cuarenta_seis,
                                                                             'pregunta_cuarenta_siete': pregunta_cuarenta_siete,
                                                                             'pregunta_cuarenta_ocho': pregunta_cuarenta_ocho,
                                                                             'pregunta_cuarenta_nueve': pregunta_cuarenta_nueve,
                                                                             'pregunta_cincuenta': pregunta_cincuenta,
                                                                             'pregunta_cincuenta_uno': pregunta_cincuenta_uno,
                                                                             'pregunta_cincuenta_dos': pregunta_cincuenta_dos,
                                                                             'pregunta_cincuenta_tres': pregunta_cincuenta_tres,
                                                                             'pregunta_cincuenta_cuatro': pregunta_cincuenta_cuatro,
                                                                             'pregunta_cincuenta_cinco': pregunta_cincuenta_cinco,
                                                                             'pregunta_cincuenta_seis': pregunta_cincuenta_seis,
                                                                             'pregunta_cincuenta_siete': pregunta_cincuenta_siete,
                                                                             'pregunta_cincuenta_ocho': pregunta_cincuenta_ocho,
                                                                             'pregunta_cincuenta_nueve': pregunta_cincuenta_nueve,
                                                                             'pregunta_sesenta': pregunta_sesenta})


def parteCuatro(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_sesenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='61').first()
    pregunta_sesenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='62').first()
    pregunta_sesenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='63').first()
    pregunta_sesenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='64').first()
    pregunta_sesenta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='65').first()
    pregunta_sesenta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='66').first()
    pregunta_sesenta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='67').first()
    pregunta_sesenta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='68').first()
    pregunta_sesenta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='69').first()
    pregunta_setenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='70').first()
    pregunta_setenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='71').first()
    pregunta_setenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='72').first()
    pregunta_setenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='73').first()
    pregunta_setenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='74').first()
    pregunta_setenta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='75').first()
    pregunta_setenta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='76').first()
    pregunta_setenta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='77').first()
    pregunta_setenta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='78').first()
    pregunta_setenta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='79').first()
    pregunta_ochenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='80').first()
    if request.method == "POST":
        preguntaSesentayUno = request.POST.get('preguntaSesentayUno', None)
        preguntaSesentayDos = request.POST.get('preguntaSesentayDos', None)
        preguntaSesentayTres = request.POST.get('preguntaSesentayTres', None)
        preguntaSesentayCuatro = request.POST.get('preguntaSesentayCuatro', None)
        preguntaSesentayCinco = request.POST.get('preguntaSesentayCinco', None)
        preguntaSesentaySeis = request.POST.get('preguntaSesentaySeis', None)
        preguntaSesentaySiete = request.POST.get('preguntaSesentaySiete', None)
        preguntaSesentayOcho = request.POST.get('preguntaSesentayOcho', None)
        preguntaSesentayNueve = request.POST.get('preguntaSesentayNueve', None)
        preguntaSetenta = request.POST.get('preguntaSetenta', None)
        preguntaSetentayUno = request.POST.get('preguntaSetentayUno', None)
        preguntaSetentayDos = request.POST.get('preguntaSetentayDos', None)
        preguntaSetentayTres = request.POST.get('preguntaSetentayTres', None)
        preguntaSetentayCuatro = request.POST.get('preguntaSetentayCuatro', None)
        preguntaSetentayCinco = request.POST.get('preguntaSetentayCinco', None)
        preguntaSetentaySeis = request.POST.get('preguntaSetentaySeis', None)
        preguntaSetentaySiete = request.POST.get('preguntaSetentaySiete', None)
        preguntaSetentayOcho = request.POST.get('preguntaSetentayOcho', None)
        preguntaSetentayNueve = request.POST.get('preguntaSetentayNueve', None)
        preguntaOchenta = request.POST.get('preguntaOchenta', None)
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='61')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='62')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='63')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='64')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='65')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='66')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='67')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='68')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='69')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='70')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='71')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='72')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='73')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='74')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='75')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='76')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='77')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='78')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='79')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='80')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchenta
        respuesta.save()
        return redirect('Eneagrama:parteCinco')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_4.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_sesenta_uno': pregunta_sesenta_uno,
                                                                             'pregunta_sesenta_dos': pregunta_sesenta_dos,
                                                                             'pregunta_sesenta_tres': pregunta_sesenta_tres,
                                                                             'pregunta_sesenta_cuatro': pregunta_sesenta_cuatro,
                                                                             'pregunta_sesenta_cinco': pregunta_sesenta_cinco,
                                                                             'pregunta_sesenta_seis': pregunta_sesenta_seis,
                                                                             'pregunta_sesenta_siete': pregunta_sesenta_siete,
                                                                             'pregunta_sesenta_ocho': pregunta_sesenta_ocho,
                                                                             'pregunta_sesenta_nueve': pregunta_sesenta_nueve,
                                                                             'pregunta_setenta': pregunta_setenta,
                                                                             'pregunta_setenta_uno': pregunta_setenta_uno,
                                                                             'pregunta_setenta_dos': pregunta_setenta_dos,
                                                                             'pregunta_setenta_tres': pregunta_setenta_tres,
                                                                             'pregunta_setenta_cuatro': pregunta_setenta_cuatro,
                                                                             'pregunta_setenta_cinco': pregunta_setenta_cinco,
                                                                             'pregunta_setenta_seis': pregunta_setenta_seis,
                                                                             'pregunta_setenta_siete': pregunta_setenta_siete,
                                                                             'pregunta_setenta_ocho': pregunta_setenta_ocho,
                                                                             'pregunta_setenta_nueve': pregunta_setenta_nueve,
                                                                             'pregunta_ochenta': pregunta_ochenta})


def parteCinco(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_ochenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='81').first()
    pregunta_ochenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='82').first()
    pregunta_ochenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='83').first()
    pregunta_ochenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='84').first()
    pregunta_ochenta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='85').first()
    pregunta_ochenta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='86').first()
    pregunta_ochenta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='87').first()
    pregunta_ochenta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='88').first()
    pregunta_ochenta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='89').first()
    pregunta_noventa = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='90').first()
    pregunta_noventa_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='91').first()
    pregunta_noventa_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='92').first()
    pregunta_noventa_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='93').first()
    pregunta_noventa_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='94').first()
    pregunta_noventa_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='95').first()
    pregunta_noventa_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='96').first()
    pregunta_noventa_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='97').first()
    pregunta_noventa_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='98').first()
    pregunta_noventa_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='99').first()
    pregunta_cien = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='100').first()
    if request.method == "POST":
        preguntaOchentayUno = request.POST.get('preguntaOchentayUno', None)
        preguntaOchentayDos = request.POST.get('preguntaOchentayDos', None)
        preguntaOchentayTres = request.POST.get('preguntaOchentayTres', None)
        preguntaOchentayCuatro = request.POST.get('preguntaOchentayCuatro', None)
        preguntaOchentayCinco = request.POST.get('preguntaOchentayCinco', None)
        preguntaOchentaySeis = request.POST.get('preguntaOchentaySeis', None)
        preguntaOchentaySiete = request.POST.get('preguntaOchentaySiete', None)
        preguntaOchentayOcho = request.POST.get('preguntaOchentayOcho', None)
        preguntaOchentayNueve = request.POST.get('preguntaOchentayNueve', None)
        preguntaNoventa = request.POST.get('preguntaNoventa', None)
        preguntaNoventayUno = request.POST.get('preguntaNoventayUno', None)
        preguntaNoventayDos = request.POST.get('preguntaNoventayDos', None)
        preguntaNoventayTres = request.POST.get('preguntaNoventayTres', None)
        preguntaNoventayCuatro = request.POST.get('preguntaNoventayCuatro', None)
        preguntaNoventayCinco = request.POST.get('preguntaNoventayCinco', None)
        preguntaNoventaySeis = request.POST.get('preguntaNoventaySeis', None)
        preguntaNoventaySiete = request.POST.get('preguntaNoventaySiete', None)
        preguntaNoventayOcho = request.POST.get('preguntaNoventayOcho', None)
        preguntaNoventayNueve = request.POST.get('preguntaNoventayNueve', None)
        preguntaCien = request.POST.get('preguntaCien', None)
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='81')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='82')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='83')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='84')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='85')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='86')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='87')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='88')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='89')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='90')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventa
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='91')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='92')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='93')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='94')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='95')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='96')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='97')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='98')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='99')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='100')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCien
        respuesta.save()
        return redirect('Eneagrama:parteSeis')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_5.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_ochenta_uno': pregunta_ochenta_uno,
                                                                             'pregunta_ochenta_dos': pregunta_ochenta_dos,
                                                                             'pregunta_ochenta_tres': pregunta_ochenta_tres,
                                                                             'pregunta_ochenta_cuatro': pregunta_ochenta_cuatro,
                                                                             'pregunta_ochenta_cinco': pregunta_ochenta_cinco,
                                                                             'pregunta_ochenta_seis': pregunta_ochenta_seis,
                                                                             'pregunta_ochenta_siete': pregunta_ochenta_siete,
                                                                             'pregunta_ochenta_ocho': pregunta_ochenta_ocho,
                                                                             'pregunta_ochenta_nueve': pregunta_ochenta_nueve,
                                                                             'pregunta_noventa': pregunta_noventa,
                                                                             'pregunta_noventa_uno': pregunta_noventa_uno,
                                                                             'pregunta_noventa_dos': pregunta_noventa_dos,
                                                                             'pregunta_noventa_tres': pregunta_noventa_tres,
                                                                             'pregunta_noventa_cuatro': pregunta_noventa_cuatro,
                                                                             'pregunta_noventa_cinco': pregunta_noventa_cinco,
                                                                             'pregunta_noventa_seis': pregunta_noventa_seis,
                                                                             'pregunta_noventa_siete': pregunta_noventa_siete,
                                                                             'pregunta_noventa_ocho': pregunta_noventa_ocho,
                                                                             'pregunta_noventa_nueve': pregunta_noventa_nueve,
                                                                             'pregunta_cien': pregunta_cien})


def parteSeis(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_cien_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='101').first()
    pregunta_cien_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='102').first()
    pregunta_cien_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='103').first()
    pregunta_cien_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='104').first()
    pregunta_cien_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='105').first()
    pregunta_cien_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='106').first()
    pregunta_cien_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='107').first()
    pregunta_cien_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='108').first()
    pregunta_cien_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='109').first()
    pregunta_cien_diez = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='110').first()
    pregunta_cien_diez_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='111').first()
    pregunta_cien_diez_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='112').first()
    pregunta_cien_diez_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='113').first()
    pregunta_cien_diez_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='114').first()
    pregunta_cien_diez_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='115').first()
    pregunta_cien_diez_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='116').first()
    pregunta_cien_diez_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='117').first()
    pregunta_cien_diez_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='118').first()
    pregunta_cien_diez_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='119').first()
    pregunta_cien_veinte = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='120').first()
    pregunta_cien_veinte_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='121').first()
    pregunta_cien_veinte_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='122').first()
    if request.method == "POST":
        preguntaCientoUno = request.POST.get('preguntaCientoUno', None)
        preguntaCientoDos = request.POST.get('preguntaCientoDos', None)
        preguntaCientoTres = request.POST.get('preguntaCientoTres', None)
        preguntaCientoCuatro = request.POST.get('preguntaCientoCuatro', None)
        preguntaCientoCinco = request.POST.get('preguntaCientoCinco', None)
        preguntaCientoSeis = request.POST.get('preguntaCientoSeis', None)
        preguntaCientoSiete = request.POST.get('preguntaCientoSiete', None)
        preguntaCientoOcho = request.POST.get('preguntaCientoOcho', None)
        preguntaCientoNueve = request.POST.get('preguntaCientoNueve', None)
        preguntaCientoDiez = request.POST.get('preguntaCientoDiez', None)
        preguntaCientoOnce = request.POST.get('preguntaCientoOnce', None)
        preguntaCientoDoce = request.POST.get('preguntaCientoDoce', None)
        preguntaCientoTrece = request.POST.get('preguntaCientoTrece', None)
        preguntaCientoCatorce = request.POST.get('preguntaCientoCatorce', None)
        preguntaCientoQuince = request.POST.get('preguntaCientoQuince', None)
        preguntaCientoDieciseis = request.POST.get('preguntaCientoDieciseis', None)
        preguntaCientoDiecisiete = request.POST.get('preguntaCientoDiecisiete', None)
        preguntaCientoDieciocho = request.POST.get('preguntaCientoDieciocho', None)
        preguntaCientoDiecinueve = request.POST.get('preguntaCientoDiecinueve', None)
        preguntaCientoVeinte = request.POST.get('preguntaCientoVeinte', None)
        preguntaCientoVeinteyUno = request.POST.get('preguntaCientoVeinteyUno', None)
        preguntaCientoVeinteyDos = request.POST.get('preguntaCientoVeinteyDos', None)
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='101')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='102')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='103')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='104')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='105')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='106')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='107')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='108')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='109')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='110')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiez
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='111')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoOnce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='112')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDoce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='113')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTrece
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='114')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCatorce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='115')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoQuince
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='116')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDieciseis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='117')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiecisiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='118')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDieciocho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='119')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiecinueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='120')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinte
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='121')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinteyUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='122')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinteyDos
        respuesta.save()
        return redirect('Eneagrama:parteSiete')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_6.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_cien_uno': pregunta_cien_uno,
                                                                             'pregunta_cien_dos': pregunta_cien_dos,
                                                                             'pregunta_cien_tres': pregunta_cien_tres,
                                                                             'pregunta_cien_cuatro': pregunta_cien_cuatro,
                                                                             'pregunta_cien_cinco': pregunta_cien_cinco,
                                                                             'pregunta_cien_seis': pregunta_cien_seis,
                                                                             'pregunta_cien_siete': pregunta_cien_siete,
                                                                             'pregunta_cien_ocho': pregunta_cien_ocho,
                                                                             'pregunta_cien_nueve': pregunta_cien_nueve,
                                                                             'pregunta_cien_diez': pregunta_cien_diez,
                                                                             'pregunta_cien_diez_uno': pregunta_cien_diez_uno,
                                                                             'pregunta_cien_diez_dos': pregunta_cien_diez_dos,
                                                                             'pregunta_cien_diez_tres': pregunta_cien_diez_tres,
                                                                             'pregunta_cien_diez_cuatro': pregunta_cien_diez_cuatro,
                                                                             'pregunta_cien_diez_cinco': pregunta_cien_diez_cinco,
                                                                             'pregunta_cien_diez_seis': pregunta_cien_diez_seis,
                                                                             'pregunta_cien_diez_siete': pregunta_cien_diez_siete,
                                                                             'pregunta_cien_diez_ocho': pregunta_cien_diez_ocho,
                                                                             'pregunta_cien_diez_nueve': pregunta_cien_diez_nueve,
                                                                             'pregunta_cien_veinte': pregunta_cien_veinte,
                                                                             'pregunta_cien_veinte_uno': pregunta_cien_veinte_uno,
                                                                             'pregunta_cien_veinte_dos': pregunta_cien_veinte_dos})


def parteSiete(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
    preguntas = float((preguntas * 100) / 144)
    preguntas = float(("%0.2f" % preguntas))
    pregunta_cien_veinte_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='123').first()
    pregunta_cien_veinte_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='124').first()
    pregunta_cien_veinte_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='125').first()
    pregunta_cien_veinte_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='126').first()
    pregunta_cien_veinte_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='127').first()
    pregunta_cien_veinte_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='128').first()
    pregunta_cien_veinte_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='129').first()
    pregunta_cien_treinta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='130').first()
    pregunta_cien_treinta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='131').first()
    pregunta_cien_treinta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='132').first()
    pregunta_cien_treinta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='133').first()
    pregunta_cien_treinta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='134').first()
    pregunta_cien_treinta_cinco = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='135').first()
    pregunta_cien_treinta_seis = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='136').first()
    pregunta_cien_treinta_siete = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='137').first()
    pregunta_cien_treinta_ocho = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='138').first()
    pregunta_cien_treinta_nueve = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='139').first()
    pregunta_cien_cuarenta = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='140').first()
    pregunta_cien_cuarenta_uno = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='141').first()
    pregunta_cien_cuarenta_dos = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='142').first()
    pregunta_cien_cuarenta_tres = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='143').first()
    pregunta_cien_cuarenta_cuatro = Respuesta.objects.filter(evaluacion=evaluacion, pregunta='144').first()
    if request.method == "POST":
        preguntaCientoVeintiTres = request.POST.get('preguntaCientoVeintiTres', None)
        preguntaCientoVeintiCuatro = request.POST.get('preguntaCientoVeintiCuatro', None)
        preguntaCientoVeintiCinco = request.POST.get('preguntaCientoVeintiCinco', None)
        preguntaCientoVeintiSeis = request.POST.get('preguntaCientoVeintiSeis', None)
        preguntaCientoVeintiSiete = request.POST.get('preguntaCientoVeintiSiete', None)
        preguntaCientoVeintiOcho = request.POST.get('preguntaCientoVeintiOcho', None)
        preguntaCientoVeintiNueve = request.POST.get('preguntaCientoVeintiNueve', None)
        preguntaCientoTreinta = request.POST.get('preguntaCientoTreinta', None)
        preguntaCientoTreintayUno = request.POST.get('preguntaCientoTreintayUno', None)
        preguntaCientoTreintayDos = request.POST.get('preguntaCientoTreintayDos', None)
        preguntaCientoTreintayTres = request.POST.get('preguntaCientoTreintayTres', None)
        preguntaCientoTreintayCuatro = request.POST.get('preguntaCientoTreintayCuatro', None)
        preguntaCientoTreintayCinco = request.POST.get('preguntaCientoTreintayCinco', None)
        preguntaCientoTreintaySeis = request.POST.get('preguntaCientoTreintaySeis', None)
        preguntaCientoTreintaySiete = request.POST.get('preguntaCientoTreintaySiete', None)
        preguntaCientoTreintayOcho = request.POST.get('preguntaCientoTreintayOcho', None)
        preguntaCientoTreintayNueve = request.POST.get('preguntaCientoTreintayNueve', None)
        preguntaCientoCuarenta = request.POST.get('preguntaCientoCuarenta', None)
        preguntaCientoCuarentayUno = request.POST.get('preguntaCientoCuarentayUno', None)
        preguntaCientoCuarentayDos = request.POST.get('preguntaCientoCuarentayDos', None)
        preguntaCientoCuarentayTres = request.POST.get('preguntaCientoCuarentayTres', None)
        preguntaCientoCuarentayCuatro = request.POST.get('preguntaCientoCuarentayCuatro', None)

        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='123')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='124')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='125')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='126')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='127')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='128')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='129')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='130')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreinta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='131')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='132')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='133')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='134')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='135')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='136')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='137')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='138')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='139')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='140')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='141')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='142')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='143')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(evaluacion=evaluacion, pregunta='144')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayCuatro
        respuesta.save()
        evaluacion.fecha_creacion = datetime.now()
        evaluacion.save()
        messages.success(request, '¡Enhorabuena has compleatado la evaluacion con exito!')
        return redirect('Eneagrama:pago_formato')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_7.html', {'nombreMostrar': nombreMostrar,
                                                                             'preguntas': preguntas,
                                                                             'pregunta_cien_veinte_tres': pregunta_cien_veinte_tres,
                                                                             'pregunta_cien_veinte_cuatro': pregunta_cien_veinte_cuatro,
                                                                             'pregunta_cien_veinte_cinco': pregunta_cien_veinte_cinco,
                                                                             'pregunta_cien_veinte_seis': pregunta_cien_veinte_seis,
                                                                             'pregunta_cien_veinte_siete': pregunta_cien_veinte_siete,
                                                                             'pregunta_cien_veinte_ocho': pregunta_cien_veinte_ocho,
                                                                             'pregunta_cien_veinte_nueve': pregunta_cien_veinte_nueve,
                                                                             'pregunta_cien_treinta': pregunta_cien_treinta,
                                                                             'pregunta_cien_treinta_uno': pregunta_cien_treinta_uno,
                                                                             'pregunta_cien_treinta_dos': pregunta_cien_treinta_dos,
                                                                             'pregunta_cien_treinta_tres': pregunta_cien_treinta_tres,
                                                                             'pregunta_cien_treinta_cuatro': pregunta_cien_treinta_cuatro,
                                                                             'pregunta_cien_treinta_cinco': pregunta_cien_treinta_cinco,
                                                                             'pregunta_cien_treinta_seis': pregunta_cien_treinta_seis,
                                                                             'pregunta_cien_treinta_siete': pregunta_cien_treinta_siete,
                                                                             'pregunta_cien_treinta_ocho': pregunta_cien_treinta_ocho,
                                                                             'pregunta_cien_treinta_nueve': pregunta_cien_treinta_nueve,
                                                                             'pregunta_cien_cuarenta': pregunta_cien_cuarenta,
                                                                             'pregunta_cien_cuarenta_uno': pregunta_cien_cuarenta_uno,
                                                                             'pregunta_cien_cuarenta_dos': pregunta_cien_cuarenta_dos,
                                                                             'pregunta_cien_cuarenta_tres': pregunta_cien_cuarenta_tres,
                                                                             'pregunta_cien_cuarenta_cuatro': pregunta_cien_cuarenta_cuatro})


def pago_formato(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de obtener tu formato debes de identificarte!')
        return redirect('Eneagrama:register', (1))
    else:
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
        if preguntas < 144 and preguntas >= 122:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteSiete')
        elif preguntas < 122 and preguntas >= 100:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteSeis')
        elif preguntas < 100 and preguntas >= 80:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteCinco')
        elif preguntas < 80 and preguntas >= 60:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteCuatro')
        elif preguntas < 60 and preguntas >= 40:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteTres')
        elif preguntas < 40 and preguntas >= 20:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteDos')
        elif preguntas < 20:
            messages.warning(request, '¡Debes de completar la encuesta!')
            return redirect('Eneagrama:parteUno')
        pago = Usuario.objects.get(id=evaluacion.usuario.id)
        pago = pago.pago
        tipoUno = Respuesta.objects.filter(evaluacion=evaluacion, valor='D').count()
        tipoDos = Respuesta.objects.filter(evaluacion=evaluacion, valor='F').count()
        tipoTres = Respuesta.objects.filter(evaluacion=evaluacion, valor='C').count()
        tipoCuatro = Respuesta.objects.filter(evaluacion=evaluacion, valor='E').count()
        tipoCinco = Respuesta.objects.filter(evaluacion=evaluacion, valor='H').count()
        tipoSeis = Respuesta.objects.filter(evaluacion=evaluacion, valor='B').count()
        tipoSiete = Respuesta.objects.filter(evaluacion=evaluacion, valor='I').count()
        tipoOcho = Respuesta.objects.filter(evaluacion=evaluacion, valor='G').count()
        tipoNueve = Respuesta.objects.filter(evaluacion=evaluacion, valor='A').count()
        if tipoUno == 0 or tipoDos == 0 or tipoTres == 0 or tipoCuatro == 0 or tipoCinco == 0 or tipoSeis == 0 or tipoSiete == 0 or tipoOcho == 0 or tipoNueve == 0:
            messages.error(request, '¡Antes de obtener tu formato debes llenar la encuesta!')
            return redirect('Eneagrama:parteUno')
        else:
            evaluacion.tipoUno = tipoUno
            evaluacion.tipoDos = tipoDos
            evaluacion.tipoTres = tipoTres
            evaluacion.tipoCuatro = tipoCuatro
            evaluacion.tipoCinco = tipoCinco
            evaluacion.tipoSeis = tipoSeis
            evaluacion.tipoSiete = tipoSiete
            evaluacion.tipoOcho = tipoOcho
            evaluacion.tipoNueve = tipoNueve
            evaluacion.save()
            tipos = [tipoUno, tipoDos, tipoTres, tipoCuatro, tipoCinco, tipoSeis, tipoSiete, tipoOcho, tipoNueve]
            eneatipoPrincipal = None
            eneatipoSecundario = None
            eneatipoTerciario = None
            # ***********inicia ciclo para obtener el eneatipo************************************************************
            i = 0
            j = 1
            valor2 = 0
            valor3 = 0
            while j <= 8:
                if tipos[i] > tipos[j]:
                    eneatipoPrincipal = i + 1
                    if valor2 > tipos[j]:
                        if valor3 < tipos[j]:
                            eneatipoTerciario = j + 1
                            valor3 = tipos[j]
                    else:
                        valor3 = valor2
                        eneatipoTerciario = eneatipoSecundario
                        valor2 = tipos[j]
                        eneatipoSecundario = j + 1
                    i = i
                    j += 1
                else:
                    if valor2 > tipos[i]:
                        eneatipoTerciario = i + 1
                        valor3 = tipos[i]
                    else:
                        valor3 = valor2
                        eneatipoTerciario = eneatipoSecundario
                        valor2 = tipos[i]
                        eneatipoSecundario = i + 1
                    i = j
                    j += 1
                    eneatipoPrincipal = j
                    # *******************finaliza ciclo para obtener el eneatipos**************************************************
            evaluacion.eneatipoPrincipal = str(eneatipoPrincipal)
            evaluacion.eneatipoSecundario = str(eneatipoSecundario)
            evaluacion.eneatipoTerciario = str(eneatipoTerciario)
            evaluacion.save()
            centroFisico = tipoNueve + tipoUno + tipoOcho
            centroEmocional = tipoDos + tipoTres + tipoCuatro
            centroIntelectual = tipoCinco + tipoSeis + tipoSiete
            energiaInterna = tipoUno + tipoCuatro + tipoCinco
            energiaExterna = tipoDos + tipoSiete + tipoOcho
            energiaEquilibrio = tipoNueve + tipoTres + tipoSeis
            evaluacion.centroFisico = centroFisico
            evaluacion.centroEmocional = centroEmocional
            evaluacion.centroIntelectual = centroIntelectual
            evaluacion.energiaInterna = energiaInterna
            evaluacion.energiaExterna = energiaExterna
            evaluacion.energiaEquilibrio = energiaEquilibrio
            evaluacion.save()
            tipos = [centroEmocional, centroFisico, centroIntelectual]
            centroPrimario = None
            centroSecundario = None
            centroTerciario = None
            # ***********inicia ciclo para obtener el centros************************************************************
            i = 0
            j = 1
            valor2 = 0
            valor3 = 0
            while j <= 2:
                if tipos[i] > tipos[j]:
                    centroPrimario = i + 1
                    if valor2 > tipos[j]:
                        if valor3 < tipos[j]:
                            centroTerciario = j + 1
                            valor3 = tipos[j]
                    else:
                        valor3 = valor2
                        centroTerciario = centroSecundario
                        valor2 = tipos[j]
                        centroSecundario = j + 1
                    i = i
                    j += 1
                else:
                    if valor2 > tipos[i]:
                        centroTerciario = i + 1
                        valor3 = tipos[i]
                    else:
                        valor3 = valor2
                        centroTerciario = centroSecundario
                        valor2 = tipos[i]
                        centroSecundario = i + 1
                    i = j
                    j += 1
                    centroPrimario = j
                    # *******************finaliza ciclo para obtener el centros**************************************************
            evaluacion.centroPrimario = str(centroPrimario)
            evaluacion.centroSecundario = str(centroSecundario)
            evaluacion.centroTerciario = str(centroTerciario)
            evaluacion.save()
            tipos = [energiaInterna, energiaExterna, energiaEquilibrio]
            energiaPrimaria = None
            energiaSecundaria = None
            energiaTerciaria = None
            # ***********inicia ciclo para obtener el centros************************************************************
            i = 0
            j = 1
            valor2 = 0
            valor3 = 0
            while j <= 2:
                if tipos[i] > tipos[j]:
                    energiaPrimaria = i + 1
                    if valor2 > tipos[j]:
                        if valor3 < tipos[j]:
                            energiaTerciaria = j + 1
                            valor3 = tipos[j]
                    else:
                        valor3 = valor2
                        energiaTerciaria = energiaSecundaria
                        valor2 = tipos[j]
                        energiaSecundaria = j + 1
                    i = i
                    j += 1
                else:
                    if valor2 > tipos[i]:
                        energiaTerciaria = i + 1
                        valor3 = tipos[i]
                    else:
                        valor3 = valor2
                        energiaTerciaria = energiaSecundaria
                        valor2 = tipos[i]
                        energiaSecundaria = i + 1
                    i = j
                    j += 1
                    energiaPrimaria = j
                    # *******************finaliza ciclo para obtener el centros**************************************************
            evaluacion.energiaPrimaria = str(energiaPrimaria)
            evaluacion.energiaSecundaria = str(energiaSecundaria)
            evaluacion.energiaTerciaria = str(energiaTerciaria)
            evaluacion.save()
            comprobante = Comprobante.objects.filter(usuario=evaluacion.usuario).last()
            if comprobante.tipo_pago == '0':
                return redirect('Eneagrama:Reporte_eneagrama')
            if comprobante.tipo_pago == '1':
                subject = 'Eneagrama, resultados para: {0}'.format(evaluacion.usuario.nombre)
                html_content = get_template('eneagrama/email/formato_email.html').render({'evaluacion': evaluacion,
                                                                                          'comprobante': comprobante})

                msg = EmailMessage(
                    subject=subject,
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['manuel.chavez.carrillo@gmail.com', ],
                    cc=['c.iturriosalcaraz@gmail.com', ],
                )
                msg.content_subtype = "html"
                msg.send(fail_silently=not settings.DEBUG)

                messages.success(request, '¡{0} {1}, Imprime o guarda tu reporte!'.format(
                    evaluacion.usuario.nombre, evaluacion.usuario.apellidos))

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/pago_formato.html',
                  {'nombreMostrar': nombreMostrar, 'evaluacion': evaluacion, 'pago': pago, 'comprobante': comprobante})


@login_required()
def obtencion_de_valores(request):
    usuario = None
    evaluacion = None
    usuariosSelect = Usuario.objects.all()
    evaluaciones = Evaluacion.objects.all()
    if request.method == "POST":
        usuario = request.POST.get('usuario', None)
        usuario = Usuario.objects.get(id=usuario)
        evaluacion = Evaluacion.objects.get(usuario=usuario)

    return render(request, 'eneagrama/obtencion_de_valores.html',
                  {'evaluaciones': evaluaciones, 'usuariosSelect': usuariosSelect, 'evaluacion': evaluacion})


class Borrar_sesion(TemplateView):
    def get(self, request, *args, **kwargs):
        metodoPago = request.session['metodoPago']
        del request.session['nombre']
        del request.session['id_evaluacion']
        return redirect('Eneagrama:register', (metodoPago))


def metodo_pago(request):
    return render(request, 'eneagrama/metodo_pago.html')


def taller(request):
    codigos = Codigo.objects.filter(activo=True)
    if not codigos:
        messages.success(request, '¡Compra tu reporte eneagrama o  realiza la evaluacion gratuita!')
        messages.warning(request, '¡No hay talleres disponibles!')
        return redirect('Eneagrama:principal')
    return render(request, 'eneagrama/principal_taller.html')


def realizar_pago(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))

    nombreMostrar = request.session['nombre']
    evaluacion_id = Evaluacion.objects.get(id=request.session['id_evaluacion'])

    initial = {
        'business': settings.PAYPAL_BUSINESS,
        'currency_code': 'MXN',
        'amount': '190.00',
        'item_name': 'Encuesta eneagrama CO2LIDERAZGO',
        'invoice': '{}'.format(evaluacion_id),
        'notify_url': request.build_absolute_uri(reverse('Eneagrama:paypal-ipn')),
        'return': request.build_absolute_uri(reverse('Eneagrama:parteUno')),
        'cancel_return': request.build_absolute_uri(reverse('Eneagrama:realizar_pago')),
    }

    form_paypal = PayPalPaymentsForm(initial=initial)

    return render(request, 'eneagrama/realizar_pago.html', {'nombreMostrar': nombreMostrar, 'form_paypal': form_paypal})


def registrar_comprobante(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register', (1))
    else:
        nombreMostrar = request.session['nombre']
        if request.method == "POST":
            evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
            preguntas = Respuesta.objects.filter(evaluacion=evaluacion).count()
            fecha = request.POST.get('fecha', None)
            importe = request.POST.get('importe', None)
            metodo = request.POST.get('metodo', None)
            ficha = request.POST.get('ficha', None)
            comprobante = Comprobante.objects.filter(usuario=evaluacion.usuario).last()
            if comprobante:
                comprobante.fecha = fecha
                comprobante.importe = importe
                comprobante.tipo_pago = '3'
                comprobante.imagen_comprobante = ficha
                comprobante.metodo_pago = metodo
                comprobante.usuario = evaluacion.usuario
                comprobante.evaluacion = evaluacion
                comprobante.save()

                usuario = Usuario.objects.get(id=evaluacion.usuario.id)
                usuario.pago = True
                usuario.save()

            else:
                comprobante = Comprobante()
                comprobante.fecha = fecha
                comprobante.importe = importe
                comprobante.tipo_pago = '3'
                comprobante.imagen_comprobante = ficha
                comprobante.metodo_pago = metodo
                comprobante.usuario = evaluacion.usuario
                comprobante.evaluacion = evaluacion
                comprobante.save()

                usuario = Usuario.objects.get(id=evaluacion.usuario.id)
                usuario.pago = True
                usuario.save()

            if preguntas < 144:
                return redirect('Eneagrama:parteUno')
            else:
                return redirect('Eneagrama:pago_formato')
    return render(request, 'eneagrama/registrar_comprobante.html', {'nombreMostrar': nombreMostrar})


def registra_pago_paypal(request):
    pass


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'eneagrama/404_not_found.html', data)


def Reporte_eneagrama(request):
    evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
    usuario = Usuario.objects.get(id=evaluacion.usuario.id)
    if usuario.pago == False:
        messages.error(request, 'Debes de pagar el formato antes de obtenerlo.')
        return redirect('Eneagrama:pago_formato')
    else:
        comprobante = Comprobante.objects.filter(evaluacion=evaluacion, usuario=usuario).last()
        if comprobante.tipo_pago == '0':
            messages.success(request, 'El reporte te sera entregado el 24 de noviembre del 2018 en el taller.')
            subject = 'Eneagrama, resultados para: {0}'.format(evaluacion.usuario.nombre)
            html_content = get_template('eneagrama/email/formato_email.html').render({'evaluacion': evaluacion,
                                                                                      'comprobante': comprobante})

            msg = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['manuel.chavez.carrillo@gmail.com', ],
                cc=['c.iturriosalcaraz@gmail.com', ],
            )
            msg.content_subtype = "html"
            msg.send(fail_silently=not settings.DEBUG)

            usuario.pago = False
            usuario.save()

            nuevaEvaluacion = Evaluacion()
            nuevaEvaluacion.usuario = evaluacion.usuario
            nuevaEvaluacion.save()

            comprobante = Comprobante()
            comprobante.usuario = evaluacion.usuario
            comprobante.evaluacion = nuevaEvaluacion
            comprobante.save()

            del request.session['nombre']
            del request.session['id_evaluacion']

            return redirect('Eneagrama:taller')

        elif comprobante.tipo_pago == '3':
            messages.success(request, 'Estamos verificando tu comprobante de pago, una vez validado '
                                      'te enviaremos el reporte a tu correo.')
            subject = 'Eneagrama, resultados para: {0}'.format(evaluacion.usuario.nombre)
            html_content = get_template('eneagrama/email/formato_email.html').render({'evaluacion': evaluacion,
                                                                                      'comprobante': comprobante})

            msg = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['manuel.chavez.carrillo@gmail.com', ],
                cc=['c.iturriosalcaraz@gmail.com', ],
            )
            msg.content_subtype = "html"
            msg.send(fail_silently=not settings.DEBUG)

            usuario.pago = False
            usuario.save()

            nuevaEvaluacion = Evaluacion()
            nuevaEvaluacion.usuario = evaluacion.usuario
            nuevaEvaluacion.save()

            comprobante = Comprobante()
            comprobante.usuario = evaluacion.usuario
            comprobante.evaluacion = nuevaEvaluacion
            comprobante.save()
            del request.session['nombre']
            del request.session['id_evaluacion']

            return redirect('Eneagrama:principal')
        #################################### DATOS #################################################
        eneatipoPrincipal = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoPrincipal)
        eneatipoSecundario = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoSecundario)
        eneatipoTerciario = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoTerciario)
        centro_descripciones = Centro.objects.filter(centro=evaluacion.centroPrimario)
        energia_descripciones = Energia.objects.filter(energia=evaluacion.eneatipoPrincipal)
        diccionarioUno = {'tipo': '1. Perfeccionista', 'total': evaluacion.tipoUno}
        diccionarioDos = {'tipo': '2. Colaborador', 'total': evaluacion.tipoDos}
        diccionarioTres = {'tipo': '3. Competitivo', 'total': evaluacion.tipoTres}
        diccionarioCuatro = {'tipo': '4. Creativo', 'total': evaluacion.tipoCuatro}
        diccionarioCinco = {'tipo': '5. Analítico', 'total': evaluacion.tipoCinco}
        diccionarioSeis = {'tipo': '6. Comprometido', 'total': evaluacion.tipoSeis}
        diccionarioSiete = {'tipo': '7. Dinámico', 'total': evaluacion.tipoSiete}
        diccionarioOcho = {'tipo': '8. Líder', 'total': evaluacion.tipoOcho}
        diccionarioNueve = {'tipo': '9. Conciliador', 'total': evaluacion.tipoNueve}
        lista = [diccionarioUno, diccionarioDos, diccionarioTres, diccionarioCuatro, diccionarioCinco,
                 diccionarioSeis, diccionarioSiete, diccionarioOcho, diccionarioNueve]
        newList = lista
        listaOrdenada = sorted(lista, key=lambda k: k['total'])
        ##################################### DATOS #################################################
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="ReporteEneagrama.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("Reporte eneagrama {0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        p.setLineWidth(.3)

        if evaluacion.fecha_creacion.month == 1:
            mes = 'Enero'
        elif evaluacion.fecha_creacion.month == 2:
            mes = 'Febrero'
        elif evaluacion.fecha_creacion.month == 3:
            mes = 'Marzo'
        elif evaluacion.fecha_creacion.month == 4:
            mes = 'Abril'
        elif evaluacion.fecha_creacion.month == 5:
            mes = 'Mayo'
        elif evaluacion.fecha_creacion.month == 6:
            mes = 'Junio'
        elif evaluacion.fecha_creacion.month == 7:
            mes = 'Julio'
        elif evaluacion.fecha_creacion.month == 8:
            mes = 'Agosto'
        elif evaluacion.fecha_creacion.month == 9:
            mes = 'Septiembre'
        elif evaluacion.fecha_creacion.month == 10:
            mes = 'Octubre'
        elif evaluacion.fecha_creacion.month == 11:
            mes = 'Noviembre'
        elif evaluacion.fecha_creacion.month == 12:
            mes = 'Diciembre'

        date_time = "{0} {1}, {2}".format(mes, evaluacion.fecha_creacion.day, evaluacion.fecha_creacion.year)

        azul = colors.Color(0, 0.1803921568627, 0.3647058823529)
        p.setStrokeColor(azul)
        p.setFillColor(azul)
        p.setFont('Helvetica-Bold', 18)

        template = ImageReader(settings.MEDIA_ROOT + '/excel/portada.png')
        p.drawImage(template, 27, 18, 565, 755, mask='auto')
        nombre = evaluacion.usuario.nombre + ' ' + evaluacion.usuario.apellidos
        p.drawCentredString(305, 390, "{0}".format(nombre))
        p.setFont('Helvetica-Bold', 13)
        p.drawCentredString(305, 360, "{0}".format(date_time))

        p.showPage()
        ############################################## portada ###################################################3
        fondo_azul = ImageReader(settings.MEDIA_ROOT + '/excel/fondo_azul.png')
        template = ImageReader(settings.MEDIA_ROOT + '/excel/pagina_2_la2.png')
        p.drawImage(template, 0, 0, 610, 791, mask='auto')
        p.setFont('Helvetica-Bold', 10)

        p.drawCentredString(305, 745, "{0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))

        if newList[8]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/9_coinciliador_tabla.png')
        elif newList[0]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/1_perfeccionista_tabla.png')
        elif newList[1]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/2_colaborador_tabla.png')
        elif newList[2]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/3_competitivo_tabla.png')
        elif newList[3]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/4_creativo_tabla.png')
        elif newList[4]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/5_analitico_tabla.png')
        elif newList[5]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/6_comprometido_tabla.png')
        elif newList[6]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/7_dinamico_tabla.png')
        else:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/8_lider_tabla.png')

        p.drawImage(tabla, 36, 488, 198, 196, mask='auto')

        p.drawString(41, 645, "{0}".format(newList[8]['tipo']))
        p.drawString(181, 645, "{0}".format(newList[8]['total']))

        p.drawString(41, 626, "{0}".format(newList[0]['tipo']))
        p.drawString(181, 626, "{0}".format(newList[0]['total']))

        p.drawString(41, 608, "{0}".format(newList[1]['tipo']))
        p.drawString(181, 608, "{0}".format(newList[1]['total']))

        p.drawString(41, 590, "{0}".format(newList[2]['tipo']))
        p.drawString(181, 590, "{0}".format(newList[2]['total']))

        p.drawString(41, 571, "{0}".format(newList[3]['tipo']))
        p.drawString(181, 571, "{0}".format(newList[3]['total']))

        p.drawString(41, 552, "{0}".format(newList[4]['tipo']))
        p.drawString(181, 552, "{0}".format(newList[4]['total']))

        p.drawString(41, 534, "{0}".format(newList[5]['tipo']))
        p.drawString(181, 534, "{0}".format(newList[5]['total']))

        p.drawString(41, 514, "{0}".format(newList[6]['tipo']))
        p.drawString(181, 514, "{0}".format(newList[6]['total']))

        p.drawString(41, 496, "{0}".format(newList[7]['tipo']))
        p.drawString(181, 496, "{0}".format(newList[7]['total']))

        d = Drawing(400, 400)
        sp = SpiderChart()
        sp.x = 50
        sp.y = 50
        sp.width = 190
        sp.height = 190
        sp.data = [[35, 35, 35, 35, 35, 35, 35, 35, 35], [25, 25, 25, 25, 25, 25, 25, 25, 25],
                   [20, 20, 20, 20, 20, 20, 20, 20, 20],
                   [15, 15, 15, 15, 15, 15, 15, 15, 15], [10, 10, 10, 10, 10, 10, 10, 10, 10],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [newList[8]['total'], newList[0]['total'], newList[1]['total'],
                    newList[2]['total'], newList[3]['total'], newList[4]['total'],
                    newList[5]['total'], newList[6]['total'], newList[7]['total']]]
        sp.labels = ['9. Conciliador', '1. Perfeccionista', '2. Colaborador', '3. Competitivo',
                     '4. Creativo', '5. Analítico', '6. Comprometido', '7. Dinámico', '8. Líder']
        sp.spokeLabels.fontName = 'Helvetica-Bold'
        sp.spokeLabels.fontSize = 8
        grey_transparent = colors.Color(0.6705882352941, 0.6823529411764, 0.69803992156862, 0.2)
        sp.strands[0].strokeColor = colors.white
        azulito = colors.Color(0.356862745098, 0.556862745098, 0.8)
        azulito_contorno = colors.Color(0.2235294117647, 0.356862745098, 0.8392156862745)
        sp.strands[6].strokeColor = azulito_contorno
        sp.strands[6].fillColor = azulito
        sp.spokes.strokeDashArray = (0, 999)
        sp.strands[1].strokeColor = grey_transparent
        sp.strands[2].strokeColor = grey_transparent
        sp.strands[3].strokeColor = grey_transparent
        sp.strands[4].strokeColor = grey_transparent
        sp.strands[5].strokeColor = grey_transparent
        d.add(sp)

        d.drawOn(p, 290, 431)

        tabla = ImageReader(settings.MEDIA_ROOT + '/excel/eneatipos_tabla.png')

        p.drawImage(tabla, 36, 362, 180, 90, mask='auto')

        p.drawString(40, 412, "{0}".format(listaOrdenada[8]['tipo']))
        p.drawString(166, 412, "{0}".format(listaOrdenada[8]['total']))
        p.drawString(40, 391, "{0}".format(listaOrdenada[7]['tipo']))
        p.drawString(166, 391, "{0}".format(listaOrdenada[7]['total']))
        p.drawString(40, 369, "{0}".format(listaOrdenada[6]['tipo']))
        p.drawString(166, 369, "{0}".format(listaOrdenada[6]['total']))

        drawing = Drawing(400, 200)
        data = [(listaOrdenada[8]['total'], listaOrdenada[7]['total'], listaOrdenada[6]['total'])]
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 280
        bc.data = data

        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 28
        bc.valueAxis.valueStep = 10
        bc.categoryAxis.labels.angle = 0
        bc.categoryAxis.categoryNames = [listaOrdenada[8]['tipo'], listaOrdenada[7]['tipo'], listaOrdenada[6]['tipo']]
        bc.categoryAxis.labels.fontName = 'Helvetica-Bold'
        bc.bars[0].fillColor = azulito
        bc.bars[0].strokeColor = azulito_contorno
        bc.valueAxis.labels.fontSize = 0
        bc.valueAxis.strokeColor = colors.white
        bc.categoryAxis.strokeColor = colors.white
        drawing.add(bc)

        drawing.drawOn(p, 235, 315)

        p.setStrokeColor(colors.black)

        alto = 310

        p.drawImage(fondo_azul, 36, 314, 538, 40, mask='auto')
        p.drawCentredString(305, 329, "{0}".format(listaOrdenada[8]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoPrincipal:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        alto = 213
        p.drawImage(fondo_azul, 36, 217, 538, 40, mask='auto')
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 232, "{0}".format(listaOrdenada[7]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoSecundario:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        alto = 112
        p.drawImage(fondo_azul, 36, 116, 538, 40, mask='auto')
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 131, "{0}".format(listaOrdenada[6]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoTerciario:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        p.showPage()
        ############################################## segunda pagina ###################################################
        template = ImageReader(settings.MEDIA_ROOT + '/excel/pagina_3.png')
        p.drawImage(template, 0, 0, 610, 791, mask='auto')

        tabla_centros = ImageReader(settings.MEDIA_ROOT + '/excel/tabla_centros.png')
        tabla_energias = ImageReader(settings.MEDIA_ROOT + '/excel/tabla_energias.png')
        p.drawImage(tabla_centros, 36, 593, 180, 90, mask='auto')

        p.setFillColor(colors.lightgrey)
        p.setStrokeColor(colors.lightgrey)
        p.rect(252, 602, 306, 72, stroke=True, fill=True)

        p.setFillColor(colors.black)
        p.setStrokeColor(colors.black)
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 745, "{0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        if evaluacion.centroPrimario == '1':
            p.drawString(188, 645, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroPrimario == '2':
            p.drawString(188, 645, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroPrimario == '3':
            p.drawString(188, 645, "{0}".format(evaluacion.centroIntelectual))
        if evaluacion.centroSecundario == '1':
            p.drawString(188, 623, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroSecundario == '2':
            p.drawString(188, 623, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroSecundario == '3':
            p.drawString(188, 623, "{0}".format(evaluacion.centroIntelectual))
        if evaluacion.centroTerciario == '1':
            p.drawString(188, 601, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroTerciario == '2':
            p.drawString(188, 601, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroTerciario == '3':
            p.drawString(188, 601, "{0}".format(evaluacion.centroIntelectual))

        p.drawString(46, 645, "{0}".format(evaluacion.get_centroPrimario_display()))
        p.drawString(46, 623, "{0}".format(evaluacion.get_centroSecundario_display()))
        p.drawString(46, 601, "{0}".format(evaluacion.get_centroTerciario_display()))
        p.setFont('Helvetica', 11)

        alto = 653
        for centro in centro_descripciones:
            p.drawString(264, alto, "{0}".format(centro.descripcion))
            alto -= 12

        p.drawImage(tabla_energias, 370, 438, 180, 90, mask='auto')

        p.setFillColor(colors.lightgrey)
        p.setStrokeColor(colors.lightgrey)
        p.rect(36, 402, 306, 162, stroke=True, fill=True)

        p.setFillColor(colors.black)
        p.setStrokeColor(colors.black)
        p.setFont('Helvetica-Bold', 10)

        p.drawString(380, 490, "{0}".format(evaluacion.get_energiaPrimaria_display()))
        p.drawString(380, 468, "{0}".format(evaluacion.get_energiaSecundaria_display()))
        p.drawString(380, 446, "{0}".format(evaluacion.get_energiaTerciaria_display()))

        if evaluacion.energiaPrimaria == '1':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaPrimaria == '2':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaPrimaria == '3':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaEquilibrio))
        if evaluacion.energiaSecundaria == '1':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaSecundaria == '2':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaSecundaria == '3':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaEquilibrio))
        if evaluacion.energiaTerciaria == '1':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaTerciaria == '2':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaTerciaria == '3':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaEquilibrio))

        p.setFont('Helvetica', 11)

        alto = 519
        for energia in energia_descripciones:
            p.drawString(45, alto, "{0}".format(energia.descripcion))
            alto -= 12

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        subject = 'Eneagrama, resultados para: {0}'.format(evaluacion.usuario.nombre)
        html_content = get_template('eneagrama/email/formato_email.html').render({'evaluacion': evaluacion,
                                                                                  'comprobante': comprobante})

        msg = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['manuel.chavez.carrillo@gmail.com', ],
            cc=['c.iturriosalcaraz@gmail.com', ],
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=not settings.DEBUG)

        messages.success(request, '¡{0} {1}, Imprime o guarda tu reporte!'.format(
            evaluacion.usuario.nombre, evaluacion.usuario.apellidos))

        usuario.pago = False
        usuario.save()

        nuevaEvaluacion = Evaluacion()
        nuevaEvaluacion.usuario = evaluacion.usuario
        nuevaEvaluacion.save()

        comprobante = Comprobante()
        comprobante.usuario = evaluacion.usuario
        comprobante.evaluacion = nuevaEvaluacion
        comprobante.save()

        del request.session['nombre']
        del request.session['id_evaluacion']

    return response


@login_required()
def write_pdf_view(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    usuario = Usuario.objects.get(id=evaluacion.usuario.id)
    if evaluacion.evaluacion_resuesta_set.count() < 144:
        messages.error(request, '¡Esta evaluacion se encuentra incompleta!')
        return redirect('Eneagrama:Dashboard')
    else:
        #################################### DATOS #################################################
        eneatipoPrincipal = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoPrincipal)
        eneatipoSecundario = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoSecundario)
        eneatipoTerciario = Eneatipo.objects.filter(eneatipo=evaluacion.eneatipoTerciario)
        centro_descripciones = Centro.objects.filter(centro=evaluacion.centroPrimario)
        energia_descripciones = Energia.objects.filter(energia=evaluacion.eneatipoPrincipal)
        diccionarioUno = {'tipo': '1. Perfeccionista', 'total': evaluacion.tipoUno}
        diccionarioDos = {'tipo': '2. Colaborador', 'total': evaluacion.tipoDos}
        diccionarioTres = {'tipo': '3. Competitivo', 'total': evaluacion.tipoTres}
        diccionarioCuatro = {'tipo': '4. Creativo', 'total': evaluacion.tipoCuatro}
        diccionarioCinco = {'tipo': '5. Analítico', 'total': evaluacion.tipoCinco}
        diccionarioSeis = {'tipo': '6. Comprometido', 'total': evaluacion.tipoSeis}
        diccionarioSiete = {'tipo': '7. Dinámico', 'total': evaluacion.tipoSiete}
        diccionarioOcho = {'tipo': '8. Líder', 'total': evaluacion.tipoOcho}
        diccionarioNueve = {'tipo': '9. Conciliador', 'total': evaluacion.tipoNueve}
        lista = [diccionarioUno, diccionarioDos, diccionarioTres, diccionarioCuatro, diccionarioCinco,
                 diccionarioSeis, diccionarioSiete, diccionarioOcho, diccionarioNueve]
        newList = lista
        listaOrdenada = sorted(lista, key=lambda k: k['total'])
        ##################################### DATOS #################################################
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="ReporteEneagrama.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("Reporte eneagrama {0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        p.setLineWidth(.3)

        if evaluacion.fecha_creacion.month == 1:
            mes = 'Enero'
        elif evaluacion.fecha_creacion.month == 2:
            mes = 'Febrero'
        elif evaluacion.fecha_creacion.month == 3:
            mes = 'Marzo'
        elif evaluacion.fecha_creacion.month == 4:
            mes = 'Abril'
        elif evaluacion.fecha_creacion.month == 5:
            mes = 'Mayo'
        elif evaluacion.fecha_creacion.month == 6:
            mes = 'Junio'
        elif evaluacion.fecha_creacion.month == 7:
            mes = 'Julio'
        elif evaluacion.fecha_creacion.month == 8:
            mes = 'Agosto'
        elif evaluacion.fecha_creacion.month == 9:
            mes = 'Septiembre'
        elif evaluacion.fecha_creacion.month == 10:
            mes = 'Octubre'
        elif evaluacion.fecha_creacion.month == 11:
            mes = 'Noviembre'
        elif evaluacion.fecha_creacion.month == 12:
            mes = 'Diciembre'

        date_time = "{0} {1}, {2}".format(mes, evaluacion.fecha_creacion.day, evaluacion.fecha_creacion.year)

        azul = colors.Color(0, 0.1803921568627, 0.3647058823529)
        p.setStrokeColor(azul)
        p.setFillColor(azul)
        p.setFont('Helvetica-Bold', 18)

        template = ImageReader(settings.MEDIA_ROOT + '/excel/portada.png')
        p.drawImage(template, 27, 18, 565, 755, mask='auto')
        nombre = evaluacion.usuario.nombre + ' ' + evaluacion.usuario.apellidos
        p.drawCentredString(305, 390, "{0}".format(nombre))
        p.setFont('Helvetica-Bold', 13)
        p.drawCentredString(305, 360, "{0}".format(date_time))

        p.showPage()
        ############################################## portada ###################################################3
        fondo_azul = ImageReader(settings.MEDIA_ROOT + '/excel/fondo_azul.png')
        template = ImageReader(settings.MEDIA_ROOT + '/excel/pagina_2_la2.png')
        p.drawImage(template, 0, 0, 610, 791, mask='auto')
        p.setFont('Helvetica-Bold', 10)

        p.drawCentredString(305, 745, "{0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))

        if newList[8]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/9_coinciliador_tabla.png')
        elif newList[0]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/1_perfeccionista_tabla.png')
        elif newList[1]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/2_colaborador_tabla.png')
        elif newList[2]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/3_competitivo_tabla.png')
        elif newList[3]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/4_creativo_tabla.png')
        elif newList[4]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/5_analitico_tabla.png')
        elif newList[5]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/6_comprometido_tabla.png')
        elif newList[6]['tipo'] == listaOrdenada[8]['tipo']:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/7_dinamico_tabla.png')
        else:
            tabla = ImageReader(settings.MEDIA_ROOT + '/excel/8_lider_tabla.png')

        p.drawImage(tabla, 36, 488, 198, 196, mask='auto')

        p.drawString(41, 645, "{0}".format(newList[8]['tipo']))
        p.drawString(181, 645, "{0}".format(newList[8]['total']))

        p.drawString(41, 626, "{0}".format(newList[0]['tipo']))
        p.drawString(181, 626, "{0}".format(newList[0]['total']))

        p.drawString(41, 608, "{0}".format(newList[1]['tipo']))
        p.drawString(181, 608, "{0}".format(newList[1]['total']))

        p.drawString(41, 590, "{0}".format(newList[2]['tipo']))
        p.drawString(181, 590, "{0}".format(newList[2]['total']))

        p.drawString(41, 571, "{0}".format(newList[3]['tipo']))
        p.drawString(181, 571, "{0}".format(newList[3]['total']))

        p.drawString(41, 552, "{0}".format(newList[4]['tipo']))
        p.drawString(181, 552, "{0}".format(newList[4]['total']))

        p.drawString(41, 534, "{0}".format(newList[5]['tipo']))
        p.drawString(181, 534, "{0}".format(newList[5]['total']))

        p.drawString(41, 514, "{0}".format(newList[6]['tipo']))
        p.drawString(181, 514, "{0}".format(newList[6]['total']))

        p.drawString(41, 496, "{0}".format(newList[7]['tipo']))
        p.drawString(181, 496, "{0}".format(newList[7]['total']))

        d = Drawing(400, 400)
        sp = SpiderChart()
        sp.x = 50
        sp.y = 50
        sp.width = 190
        sp.height = 190
        sp.data = [[35, 35, 35, 35, 35, 35, 35, 35, 35], [25, 25, 25, 25, 25, 25, 25, 25, 25],
                   [20, 20, 20, 20, 20, 20, 20, 20, 20],
                   [15, 15, 15, 15, 15, 15, 15, 15, 15], [10, 10, 10, 10, 10, 10, 10, 10, 10],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [newList[8]['total'], newList[0]['total'], newList[1]['total'],
                    newList[2]['total'], newList[3]['total'], newList[4]['total'],
                    newList[5]['total'], newList[6]['total'], newList[7]['total']]]
        sp.labels = ['9. Conciliador', '1. Perfeccionista', '2. Colaborador', '3. Competitivo',
                     '4. Creativo', '5. Analítico', '6. Comprometido', '7. Dinámico', '8. Líder']
        sp.spokeLabels.fontName = 'Helvetica-Bold'
        sp.spokeLabels.fontSize = 8
        grey_transparent = colors.Color(0.6705882352941, 0.6823529411764, 0.69803992156862, 0.2)
        sp.strands[0].strokeColor = colors.white
        azulito = colors.Color(0.356862745098, 0.556862745098, 0.8)
        azulito_contorno = colors.Color(0.2235294117647, 0.356862745098, 0.8392156862745)
        sp.strands[6].strokeColor = azulito_contorno
        sp.strands[6].fillColor = azulito
        sp.spokes.strokeDashArray = (0, 999)
        sp.strands[1].strokeColor = grey_transparent
        sp.strands[2].strokeColor = grey_transparent
        sp.strands[3].strokeColor = grey_transparent
        sp.strands[4].strokeColor = grey_transparent
        sp.strands[5].strokeColor = grey_transparent
        d.add(sp)

        d.drawOn(p, 290, 431)

        tabla = ImageReader(settings.MEDIA_ROOT + '/excel/eneatipos_tabla.png')

        p.drawImage(tabla, 36, 362, 180, 90, mask='auto')

        p.drawString(40, 412, "{0}".format(listaOrdenada[8]['tipo']))
        p.drawString(166, 412, "{0}".format(listaOrdenada[8]['total']))
        p.drawString(40, 391, "{0}".format(listaOrdenada[7]['tipo']))
        p.drawString(166, 391, "{0}".format(listaOrdenada[7]['total']))
        p.drawString(40, 369, "{0}".format(listaOrdenada[6]['tipo']))
        p.drawString(166, 369, "{0}".format(listaOrdenada[6]['total']))

        drawing = Drawing(400, 200)
        data = [(listaOrdenada[8]['total'], listaOrdenada[7]['total'], listaOrdenada[6]['total'])]
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 280
        bc.data = data

        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 28
        bc.valueAxis.valueStep = 10
        bc.categoryAxis.labels.angle = 0
        bc.categoryAxis.categoryNames = [listaOrdenada[8]['tipo'], listaOrdenada[7]['tipo'], listaOrdenada[6]['tipo']]
        bc.categoryAxis.labels.fontName = 'Helvetica-Bold'
        bc.bars[0].fillColor = azulito
        bc.bars[0].strokeColor = azulito_contorno
        bc.valueAxis.labels.fontSize = 0
        bc.valueAxis.strokeColor = colors.white
        bc.categoryAxis.strokeColor = colors.white
        drawing.add(bc)

        drawing.drawOn(p, 235, 315)

        p.setStrokeColor(colors.black)

        alto = 310

        p.drawImage(fondo_azul, 36, 314, 538, 40, mask='auto')
        p.drawCentredString(305, 329, "{0}".format(listaOrdenada[8]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoPrincipal:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        alto = 213
        p.drawImage(fondo_azul, 36, 217, 538, 40, mask='auto')
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 232, "{0}".format(listaOrdenada[7]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoSecundario:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        alto = 112
        p.drawImage(fondo_azul, 36, 116, 538, 40, mask='auto')
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 131, "{0}".format(listaOrdenada[6]['tipo']))
        p.setFont('Helvetica', 11)
        for principal in eneatipoTerciario:
            p.drawString(45, alto, "{0}".format(principal.descripcion))
            alto -= 12

        p.showPage()
        ############################################## segunda pagina ###################################################
        template = ImageReader(settings.MEDIA_ROOT + '/excel/pagina_3.png')
        p.drawImage(template, 0, 0, 610, 791, mask='auto')

        tabla_centros = ImageReader(settings.MEDIA_ROOT + '/excel/tabla_centros.png')
        tabla_energias = ImageReader(settings.MEDIA_ROOT + '/excel/tabla_energias.png')
        p.drawImage(tabla_centros, 36, 593, 180, 90, mask='auto')

        p.setFillColor(colors.lightgrey)
        p.setStrokeColor(colors.lightgrey)
        p.rect(252, 602, 306, 72, stroke=True, fill=True)

        p.setFillColor(colors.black)
        p.setStrokeColor(colors.black)
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(305, 745, "{0} {1}".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        if evaluacion.centroPrimario == '1':
            p.drawString(188, 645, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroPrimario == '2':
            p.drawString(188, 645, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroPrimario == '3':
            p.drawString(188, 645, "{0}".format(evaluacion.centroIntelectual))
        if evaluacion.centroSecundario == '1':
            p.drawString(188, 623, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroSecundario == '2':
            p.drawString(188, 623, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroSecundario == '3':
            p.drawString(188, 623, "{0}".format(evaluacion.centroIntelectual))
        if evaluacion.centroTerciario == '1':
            p.drawString(188, 601, "{0}".format(evaluacion.centroEmocional))
        elif evaluacion.centroTerciario == '2':
            p.drawString(188, 601, "{0}".format(evaluacion.centroFisico))
        elif evaluacion.centroTerciario == '3':
            p.drawString(188, 601, "{0}".format(evaluacion.centroIntelectual))

        p.drawString(46, 645, "{0}".format(evaluacion.get_centroPrimario_display()))
        p.drawString(46, 623, "{0}".format(evaluacion.get_centroSecundario_display()))
        p.drawString(46, 601, "{0}".format(evaluacion.get_centroTerciario_display()))
        p.setFont('Helvetica', 11)

        alto = 653
        for centro in centro_descripciones:
            p.drawString(264, alto, "{0}".format(centro.descripcion))
            alto -= 12

        p.drawImage(tabla_energias, 370, 438, 180, 90, mask='auto')

        p.setFillColor(colors.lightgrey)
        p.setStrokeColor(colors.lightgrey)
        p.rect(36, 402, 306, 162, stroke=True, fill=True)

        p.setFillColor(colors.black)
        p.setStrokeColor(colors.black)
        p.setFont('Helvetica-Bold', 10)

        p.drawString(380, 490, "{0}".format(evaluacion.get_energiaPrimaria_display()))
        p.drawString(380, 468, "{0}".format(evaluacion.get_energiaSecundaria_display()))
        p.drawString(380, 446, "{0}".format(evaluacion.get_energiaTerciaria_display()))

        if evaluacion.energiaPrimaria == '1':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaPrimaria == '2':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaPrimaria == '3':
            p.drawString(522, 490, "{0}".format(evaluacion.energiaEquilibrio))
        if evaluacion.energiaSecundaria == '1':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaSecundaria == '2':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaSecundaria == '3':
            p.drawString(522, 468, "{0}".format(evaluacion.energiaEquilibrio))
        if evaluacion.energiaTerciaria == '1':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaInterna))
        elif evaluacion.energiaTerciaria == '2':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaExterna))
        elif evaluacion.energiaTerciaria == '3':
            p.drawString(522, 446, "{0}".format(evaluacion.energiaEquilibrio))

        p.setFont('Helvetica', 11)

        alto = 519
        for energia in energia_descripciones:
            p.drawString(45, alto, "{0}".format(energia.descripcion))
            alto -= 12

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

    return response


@login_required()
def Dashboard(request):
    codigos = Codigo.objects.all()
    evaluaciones = Evaluacion.objects.all()
    comprobantes = Comprobante.objects.filter(tipo_pago='3')
    return render(request, 'eneagrama/dashboard.html', {'codigos': codigos, 'evaluaciones': evaluaciones,
                                                        'comprobantes': comprobantes})


@login_required()
def Modificar_codigo(request, pk):
    codigo = get_object_or_404(Codigo, pk=pk)
    if request.method == "POST":
        codigo_descripcion = request.POST.get('codigo', None)
        activo = request.POST.get('activo', None)
        codigo.codigo = codigo_descripcion
        if activo:
            codigo.activo = True
        else:
            codigo.activo = False
        codigo.save()

        messages.success(request, '¡El codigo ha sido actualizado con exito!')
        return redirect('Eneagrama:Dashboard')
    return render(request, 'eneagrama/modificar_codigo.html', {'codigo': codigo})


@login_required()
def Crear_codigo(request):
    if request.method == "POST":
        codigo = Codigo()
        codigo_descripcion = request.POST.get('codigo', None)
        activo = request.POST.get('activo', None)
        codigo.codigo = codigo_descripcion
        if activo:
            codigo.activo = True
        else:
            codigo.activo = False
        codigo.save()

        messages.success(request, '¡El codigo ha sido creado con exito!')
        return redirect('Eneagrama:Dashboard')
    return render(request, 'eneagrama/crear_codigo.html')


@login_required()
def Comprobante_deposito(request, pk):
    comprobante = get_object_or_404(Comprobante, pk=pk)
    evaluacion = Evaluacion.objects.filter(usuario=comprobante.usuario).last()
    return render(request, 'eneagrama/comprobante_deposito.html',
                  {'comprobante': comprobante, 'evaluacion': evaluacion})
