# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Correo, Pregunta, Respuesta


def principal(request):
    #Vista de Carrera|Empresa
    pregunta1 =Pregunta.objects.get(area='1', posicion='1')
    pregunta2 =Pregunta.objects.get(area='1', posicion='2')
    if request.method == "POST":
        slide1 = int(request.POST.get('slide1', None))
        slide2 = int(request.POST.get('slide2', None))
        text1 = request.POST.get('text1', None)
        text2 = request.POST.get('text2', None)
        if slide1 < slide2:
            request.session['wheel'] = {'slide1': slide1, 'slide2': slide2, 'text1': text1, 'text2': text2}
            return redirect('WebPagRuedaDLV:finanzas_dinero')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'principal.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def finanzas_dinero(request):
    #Vista de Finanzas|Dinero
    pregunta1 =Pregunta.objects.get(area='2', posicion='1')
    pregunta2 =Pregunta.objects.get(area='2', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide3 = int(request.POST.get('slide3', None))
        slide4 = int(request.POST.get('slide4', None))
        text3 = request.POST.get('text3', None)
        text4 = request.POST.get('text4', None)
        if slide3 < slide4:
            wheel = request.session['wheel']
            wheel['slide3'] = slide3
            wheel['slide4'] = slide4
            wheel['text3'] = text3
            wheel['text4'] = text4
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:salud_vitalidad')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'finanzas_dinero.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def salud_vitalidad(request):
    #Vista de Salud|Vitalidad
    pregunta1 =Pregunta.objects.get(area='3', posicion='1')
    pregunta2 =Pregunta.objects.get(area='3', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide5 = int(request.POST.get('slide5', None))
        slide6 = int(request.POST.get('slide6', None))
        text5 = request.POST.get('text5', None)
        text6 = request.POST.get('text6', None)
        if slide5 < slide6:
            wheel = request.session['wheel']
            wheel['slide5'] = slide5
            wheel['slide6'] = slide6
            wheel['text5'] = text5
            wheel['text6'] = text6
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:familia_amigos')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'salud_vitalidad.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def familia_amigos(request):
    #Vista de Familia|Amigos
    pregunta1 =Pregunta.objects.get(area='4', posicion='1')
    pregunta2 =Pregunta.objects.get(area='4', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide7 = int(request.POST.get('slide7', None))
        slide8 = int(request.POST.get('slide8', None))
        text7 = request.POST.get('text7', None)
        text8 = request.POST.get('text8', None)
        if slide7 < slide8:
            wheel = request.session['wheel']
            wheel['slide7'] = slide7
            wheel['slide8'] = slide8
            wheel['text7'] = text7
            wheel['text8'] = text8
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:register')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'familia_amigos.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def register(request):
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')

    if request.method == "POST":
        nombre = request.POST.get('username', None)
        apellidos = request.POST.get('lasname', None)
        email = request.POST.get('email', None)

        usuario = Correo()
        usuario.usuario = nombre
        usuario.apellidos = apellidos
        usuario.email = email
        usuario.save()

        return redirect('WebPagRuedaDLV:resultados')

    return render(request, 'register.html')


def resultados(request):
    slide1 = request.session['wheel']['slide1']
    slide2 = request.session['wheel']['slide2']
    carrera = float(slide1) / float(slide2)
    carrera = (1 - (carrera)) * 100
    carrera = int(carrera)
    slide3 = request.session['wheel']['slide3']
    slide4 = request.session['wheel']['slide4']
    finanzas = float(slide3) / float(slide4)
    finanzas = (1 - (finanzas)) * 100
    finanzas = int(finanzas)
    slide5 = request.session['wheel']['slide5']
    slide6 = request.session['wheel']['slide6']
    salud = float(slide5) / float(slide6)
    salud = (1 - (salud)) * 100
    salud = int(salud)
    slide7 = request.session['wheel']['slide7']
    slide8 = request.session['wheel']['slide8']
    familia = float(slide7) / float(slide8)
    familia = (1 - (familia)) * 100
    familia = int(familia)
    gap1 = slide1 + slide3 + slide5 + slide7
    gap2 = slide2 + slide4 + slide6 + slide8
    gaptotal = float(gap1) / float(gap2)
    gaptotal = (1 - (gaptotal)) * 100
    gaptotal = int(gaptotal)

    return render(
        request, 'resultados.html',
        {
            'slide1': slide1, 'slide2': slide2, 'carrera': carrera, 
            'slide3': slide3, 'slide4': slide4, 'finanzas': finanzas, 
            'slide5': slide5, 'slide6': slide6, 'salud': salud,
            'slide7': slide7, 'slide8': slide8, 'familia': familia, 
            'gaptotal': gaptotal
        }
    )


def slider(request):
    messages.success(request, 'Your password was updated successfully!')
    return render(request, 'slider.html')
