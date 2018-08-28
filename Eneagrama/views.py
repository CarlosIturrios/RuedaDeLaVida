# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse #email sender
#from django.template import Context #email sender
#from django.template.loader import render_to_string, get_template #email sender
#from django.core.mail import EmailMessage, EmailMultiAlternatives #email sender
from django.conf import settings
from django.core import signing
from django.contrib import messages

from .models import Usuario

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
        usuario = Usuario()
        usuario.nombre = nombre
        usuario.apellidos = apellidos
        usuario.email = email
        usuario.edad = edad
        usuario.empresa = empresa
        usuario.pais = pais
        usuario.ciudad = ciudad
        usuario.save()
        return redirect('Eneagrama:parteUno')

    return render(request, 'eneagrama/register.html', {'nombreMostrar':nombreMostrar})


def parteUno(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')

    else:
        if request.method == "POST":
            return redirect('Eneagrama:parteDos')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_1.html', {'nombreMostrar':nombreMostrar})


def parteDos(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')

    if request.method == "POST":
            return redirect('Eneagrama:parteTres')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_2.html', {'nombreMostrar':nombreMostrar})


def parteTres(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
    if request.method == "POST":
            return redirect('Eneagrama:parteCuatro')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_3.html', {'nombreMostrar':nombreMostrar})


def parteCuatro(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
    if request.method == "POST":
            return redirect('Eneagrama:parteCinco')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_4.html', {'nombreMostrar':nombreMostrar})


def parteCinco(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
    if request.method == "POST":
            return redirect('Eneagrama:parteSeis')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_5.html', {'nombreMostrar':nombreMostrar})


def parteSeis(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
    if request.method == "POST":
            return redirect('Eneagrama:parteSiete')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_6.html', {'nombreMostrar':nombreMostrar})


def parteSiete(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de realizar la encuesta debes de registrarte!')
        return redirect('Eneagrama:register')
    if request.method == "POST":
            return redirect('Eneagrama:principal')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_7.html', {'nombreMostrar':nombreMostrar})