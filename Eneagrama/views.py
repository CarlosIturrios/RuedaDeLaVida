# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse #email sender
# from django.template import Context #email sender
# from django.template.loader import render_to_string, get_template #email sender
# from django.core.mail import EmailMessage, EmailMultiAlternatives #email sender
from django.conf import settings
from django.core import signing
from django.contrib import messages

from .models import Usuario, Evaluacion, Respuesta


# Create your views here.
def principal(request):
    return render(request, 'eneagrama/principal.html')


def register(request):
    if 'nombre' in request.session:
        messages.success(request, '¡Bienvenido de nuevo!')
        return redirect('Eneagrama:parteUno')
    nombreMostrar = None
    if request.method == "POST":
        nombre = request.POST.get('nombre', None)
        apellidos = request.POST.get('apellidos', None)
        email = request.POST.get('email', None)
        edad = request.POST.get('edad', None)
        empresa = request.POST.get('empresa', None)
        pais = request.POST.get('pais', None)
        ciudad = request.POST.get('ciudad', None)
        request.session['nombre'] = nombre
        check_email = Usuario.objects.get(email=email)
        if check_email:
            messages.success(request, '¡Bienvenido de nuevo!')
            request.session['id_user'] = check_email.id
            evaluacion = Evaluacion.objects.get(usuario=check_email)
            request.session['id_evaluacion'] = evaluacion.id
            return redirect('Eneagrama:parteUno')
        else:
            usuario = Usuario()
            usuario.nombre = nombre
            usuario.apellidos = apellidos
            usuario.email = email
            usuario.edad = edad
            usuario.empresa = empresa
            usuario.pais = pais
            usuario.ciudad = ciudad
            usuario.save()
            evaluacion = Evaluacion()
            evaluacion.usuario = usuario
            evaluacion.save()
            request.session['id_user'] = usuario.id
            request.session['id_evaluacion'] = evaluacion.id
            return redirect('Eneagrama:parteUno')

    return render(request, 'eneagrama/register.html', {'nombreMostrar': nombreMostrar})


def parteUno(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')

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
        respuesta, created = Respuesta.objects.get_or_create(pregunta='1')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='2')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='3')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='4')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='5')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='6')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='7')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='8')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='9')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='10')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiez
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='11')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOnce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='12')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDoce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='13')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTrece
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='14')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCatorce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='15')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaQuince
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='16')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDieciseis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='17')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiecisiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='18')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDieciocho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='19')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaDiecinueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='20')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeinte
        respuesta.save()
        return redirect('Eneagrama:parteDos')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_1.html', {'nombreMostrar': nombreMostrar})


def parteDos(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')

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
        respuesta, created = Respuesta.objects.get_or_create(pregunta='21')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='22')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='23')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='24')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='25')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='26')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='27')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='28')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='29')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaVeintiNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='30')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreinta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='31')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='32')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='33')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='34')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='35')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='36')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='37')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='38')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='39')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaTreintayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='40')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarenta
        respuesta.save()
        return redirect('Eneagrama:parteTres')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_2.html', {'nombreMostrar': nombreMostrar})


def parteTres(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
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
        respuesta, created = Respuesta.objects.get_or_create(pregunta='41')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='42')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='43')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='44')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='45')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='46')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='47')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='48')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='49')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCuarentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='50')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='51')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='52')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='53')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='54')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='55')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='56')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='57')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='58')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='59')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCincuentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='60')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesenta
        respuesta.save()
        return redirect('Eneagrama:parteCuatro')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_3.html', {'nombreMostrar': nombreMostrar})


def parteCuatro(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
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
        respuesta, created = Respuesta.objects.get_or_create(pregunta='61')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='62')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='63')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='64')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='65')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='66')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='67')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='68')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='69')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSesentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='70')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='71')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='72')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='73')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='74')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='75')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='76')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='77')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='78')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='79')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaSetentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='80')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchenta
        respuesta.save()
        return redirect('Eneagrama:parteCinco')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_4.html', {'nombreMostrar': nombreMostrar})


def parteCinco(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
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
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(pregunta='81')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='82')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='83')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='84')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='85')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='86')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='87')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='88')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='89')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaOchentayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='90')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventa
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='91')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='92')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='93')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='94')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='95')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='96')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='97')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='98')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='99')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaNoventayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='100')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCien
        respuesta.save()
        return redirect('Eneagrama:parteSeis')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_5.html', {'nombreMostrar': nombreMostrar})


def parteSeis(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
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
        preguntaCientoDiecisiete = request.POST.get('preguntaCientoSiete', None)
        preguntaCientoDieciocho = request.POST.get('preguntaCientoDieciocho', None)
        preguntaCientoDiecinueve = request.POST.get('preguntaCientoDiecinueve', None)
        preguntaCientoVeinte = request.POST.get('preguntaCientoVeinte', None)
        preguntaCientoVeinteyUno = request.POST.get('preguntaCientoVeinteyUno', None)
        preguntaCientoVeinteyDos = request.POST.get('preguntaCientoVeinteyDos', None)
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(pregunta='101')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='102')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='103')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='104')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='105')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='106')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='107')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='108')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='109')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='110')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiez
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='111')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoOnce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='112')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDoce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='113')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTrece
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='114')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCatorce
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='115')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoQuince
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='116')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDieciseis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='117')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiecisiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='118')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDieciocho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='119')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoDiecinueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='120')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinte
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='121')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinteyUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='122')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeinteyDos
        respuesta.save()
        return redirect('Eneagrama:parteSiete')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_6.html', {'nombreMostrar': nombreMostrar})


def parteSiete(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
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
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        respuesta, created = Respuesta.objects.get_or_create(pregunta='123')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='124')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='125')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='126')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiSeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='127')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiSiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='128')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='129')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoVeintiNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='130')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreinta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='131')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='132')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='133')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='134')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayCuatro
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='135')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayCinco
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='136')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintaySeis
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='137')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintaySiete
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='138')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayOcho
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='139')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoTreintayNueve
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='140')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarenta
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='141')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayUno
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='142')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayDos
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='143')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayTres
        respuesta.save()
        respuesta, created = Respuesta.objects.get_or_create(pregunta='144')
        respuesta.evaluacion = evaluacion
        respuesta.valor = preguntaCientoCuarentayCuatro
        respuesta.save()
        return redirect('Eneagrama:principal')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_7.html', {'nombreMostrar': nombreMostrar})
