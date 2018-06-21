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
            return redirect('WebPagRuedaDLV:amor_relaciones')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'familia_amigos.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def amor_relaciones(request):
    #Vista de amor|relaciones
    pregunta1 =Pregunta.objects.get(area='5', posicion='1')
    pregunta2 =Pregunta.objects.get(area='5', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide9 = int(request.POST.get('slide9', None))
        slide10 = int(request.POST.get('slide10', None))
        text9 = request.POST.get('text9', None)
        text10 = request.POST.get('text10', None)
        if slide9 < slide10:
            wheel = request.session['wheel']
            wheel['slide9'] = slide9
            wheel['slide10'] = slide10
            wheel['text9'] = text9
            wheel['text10'] = text10
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:crecimiento_personal_aprendizaje')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'amor_relaciones.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def crecimiento_personal_aprendizaje(request):
    #Vista de amor|relaciones
    pregunta1 =Pregunta.objects.get(area='6', posicion='1')
    pregunta2 =Pregunta.objects.get(area='6', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide11 = int(request.POST.get('slide11', None))
        slide12 = int(request.POST.get('slide12', None))
        text11 = request.POST.get('text11', None)
        text12 = request.POST.get('text12', None)
        if slide11 < slide12:
            wheel = request.session['wheel']
            wheel['slide11'] = slide11
            wheel['slide12'] = slide12
            wheel['text11'] = text11
            wheel['text12'] = text12
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:diversion_estilo_de_vida')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'crecimiento_personal_aprendizaje.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2})


def diversion_estilo_de_vida(request):
#Vista de amor|relaciones
    pregunta1 =Pregunta.objects.get(area='7', posicion='1')
    pregunta2 =Pregunta.objects.get(area='7', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide13 = int(request.POST.get('slide13', None))
        slide14 = int(request.POST.get('slide14', None))
        text13 = request.POST.get('text13', None)
        text14 = request.POST.get('text14', None)
        if slide13 < slide14:
            wheel = request.session['wheel']
            wheel['slide13'] = slide13
            wheel['slide14'] = slide14
            wheel['text13'] = text13
            wheel['text14'] = text14
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:productividad_personal')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'diversion_estilo_de_vida.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2}) 


def productividad_personal(request):
#Vista de amor|relaciones
    pregunta1 =Pregunta.objects.get(area='8', posicion='1')
    pregunta2 =Pregunta.objects.get(area='8', posicion='2')
    if not 'wheel' in request.session:
        return redirect('WebPagRuedaDLV:principal')
    if request.method == "POST":
        slide15 = int(request.POST.get('slide15', None))
        slide16 = int(request.POST.get('slide16', None))
        text15 = request.POST.get('text15', None)
        text16 = request.POST.get('text16', None)
        if slide15 < slide16:
            wheel = request.session['wheel']
            wheel['slide15'] = slide15
            wheel['slide16'] = slide16
            wheel['text15'] = text15
            wheel['text16'] = text16
            request.session['wheel'] = wheel
            return redirect('WebPagRuedaDLV:register')
        else:
            messages.error(request, 'El primer controlador tiene que ser mayor al segundo!')
    return render(request, 'productividad_personal.html', {'pregunta1':pregunta1, 'pregunta2':pregunta2}) 

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
    if carrera < 40:
        parrafo_carrera = Respuesta.objects.get(nivel='1',area='1')
    elif carrera >= 40 and carrera < 70:
        parrafo_carrera = Respuesta.objects.get(nivel='2',area='1')
    else:
        parrafo_carrera = Respuesta.objects.get(nivel='3',area='1')
    slide3 = request.session['wheel']['slide3']
    slide4 = request.session['wheel']['slide4']
    finanzas = float(slide3) / float(slide4)
    finanzas = (1 - (finanzas)) * 100
    finanzas = int(finanzas)
    if finanzas < 40:
        parrafo_finanzas = Respuesta.objects.get(nivel='1',area='2')
    elif finanzas >= 40 and finanzas < 70:
        parrafo_finanzas = Respuesta.objects.get(nivel='2',area='2')
    else:
        parrafo_finanzas = Respuesta.objects.get(nivel='3',area='2')
    slide5 = request.session['wheel']['slide5']
    slide6 = request.session['wheel']['slide6']
    salud = float(slide5) / float(slide6)
    salud = (1 - (salud)) * 100
    salud = int(salud)
    if salud < 40:
        parrafo_salud = Respuesta.objects.get(nivel='1',area='3')
    elif salud >= 40 and salud < 70:
        parrafo_salud = Respuesta.objects.get(nivel='2',area='3')
    else:
        parrafo_salud = Respuesta.objects.get(nivel='3',area='3')
    slide7 = request.session['wheel']['slide7']
    slide8 = request.session['wheel']['slide8']
    familia = float(slide7) / float(slide8)
    familia = (1 - (familia)) * 100
    familia = int(familia)
    if familia < 40:
        parrafo_familia = Respuesta.objects.get(nivel='1',area='4')
    elif familia >= 40 and familia < 70:
        parrafo_familia = Respuesta.objects.get(nivel='2',area='4')
    else:
        parrafo_familia = Respuesta.objects.get(nivel='3',area='4')
    slide9 = request.session['wheel']['slide9']
    slide10 = request.session['wheel']['slide10']
    amor = float(slide9) / float(slide10)
    amor = (1 - (amor)) * 100
    amor = int(amor)
    if amor < 40:
        parrafo_amor = Respuesta.objects.get(nivel='1',area='5')
    elif amor >= 40 and amor < 70:
        parrafo_amor = Respuesta.objects.get(nivel='2',area='5')
    else:
        parrafo_amor = Respuesta.objects.get(nivel='3',area='5')
    slide11 = request.session['wheel']['slide11']
    slide12 = request.session['wheel']['slide12']
    crecimiento = float(slide11) / float(slide12)
    crecimiento = (1 - (crecimiento)) * 100
    crecimiento = int(crecimiento)
    if crecimiento < 40:
        parrafo_crecimiento = Respuesta.objects.get(nivel='1',area='6')
    elif crecimiento >= 40 and crecimiento < 70:
        parrafo_crecimiento = Respuesta.objects.get(nivel='2',area='6')
    else:
        parrafo_crecimiento = Respuesta.objects.get(nivel='3',area='6')
    slide13 = request.session['wheel']['slide13']
    slide14 = request.session['wheel']['slide14']
    diversion = float(slide13) / float(slide14)
    diversion = (1 - (diversion)) * 100
    diversion = int(diversion)
    if diversion < 40:
        parrafo_diversion = Respuesta.objects.get(nivel='1',area='7')
    elif diversion >= 40 and diversion < 70:
        parrafo_diversion = Respuesta.objects.get(nivel='2',area='7')
    else:
        parrafo_diversion = Respuesta.objects.get(nivel='3',area='7')
    slide15 = request.session['wheel']['slide15']
    slide16 = request.session['wheel']['slide16']
    productividad = float(slide15) / float(slide16)
    productividad = (1 - (productividad)) * 100
    productividad = int(productividad)
    if productividad < 40:
        parrafo_productividad = Respuesta.objects.get(nivel='1',area='8')
    elif diversion >= 40 and diversion < 70:
        parrafo_productividad = Respuesta.objects.get(nivel='2',area='8')
    else:
        parrafo_productividad = Respuesta.objects.get(nivel='3',area='8')
    gap1 = slide1 + slide3 + slide5 + slide7 + slide9 + slide11 + slide13 + slide15
    gap2 = slide2 + slide4 + slide6 + slide8 + slide10 + slide12 + slide14 + slide16
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
            'slide9': slide9, 'slide10': slide10, 'amor': amor,
            'slide11': slide11, 'slide12': slide12, 'crecimiento': crecimiento,
            'slide13': slide13, 'slide14': slide14, 'diversion': diversion,
            'slide15': slide15, 'slide16': slide16, 'productividad': productividad,
            'gaptotal': gaptotal, 'parrafo_carrera':parrafo_carrera, 'parrafo_finanzas':parrafo_finanzas,
            'parrafo_salud':parrafo_salud, 'parrafo_familia':parrafo_familia, 'parrafo_amor':parrafo_amor,
            'parrafo_crecimiento':parrafo_crecimiento, 'parrafo_diversion':parrafo_diversion,
            'parrafo_productividad':parrafo_productividad
        }
    )


def slider(request):
    messages.success(request, 'Your password was updated successfully!')
    return render(request, 'slider.html')
