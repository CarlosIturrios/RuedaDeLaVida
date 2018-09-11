# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse  # email sender
from django.template import Context  # email sender
from django.template.loader import render_to_string, get_template  # email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives  # email sender
from django.core import signing
from django.conf import settings
from django.views.generic import View, TemplateView
from openpyxl import Workbook, load_workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.axis import DateAxis
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.drawing.image import Image
from datetime import date
from io import BytesIO

from .models import Usuario, Evaluacion, Respuesta, Energia, Centro, Eneatipo


class ReporteExcel(TemplateView):
    def get(self, request, *args, **kwargs):
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        eneatipoPrincipal = Eneatipo.objects.get(eneatipo=evaluacion.eneatipoPrincipal)
        eneatipoSecundario = Eneatipo.objects.get(eneatipo=evaluacion.eneatipoSecundario)
        eneatipoTerciario = Eneatipo.objects.get(eneatipo=evaluacion.eneatipoTerciario)
        centro = Centro.objects.get(centro=evaluacion.centroPrimario)
        energia = Energia.objects.get(energia=evaluacion.eneatipoPrincipal)
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
        listaOrdenada  = sorted(lista, key=lambda k: k['total'])
        wb = load_workbook(settings.MEDIA_ROOT + '/excel/Template_Eneagrama.xlsx')
        ws = wb.active
        ws['B2'] = evaluacion.usuario.nombre + ' ' + evaluacion.usuario.apellidos
        ws['R2'] = evaluacion.fecha_creacion
        ws['B5'] = newList[0]['tipo']
        ws['C5'] = newList[0]['total']
        if newList[0]['tipo'] == listaOrdenada[8]['tipo']:
            B5 = ws['B5']
            C5 = ws['C5']
            ft = Font(bold=True)
            B5.font = ft
            C5.font = ft
            ws['B5'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
            ws['C5'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
        ws['B6'] = newList[1]['tipo']
        ws['C6'] = newList[1]['total']
        if newList[1]['tipo'] == listaOrdenada[8]['tipo']:
            B6 = ws['B6']
            C6 = ws['C6']
            ft = Font(bold=True)
            B6.font = ft
            C6.font = ft
            ws['B6'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
            ws['C6'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
        ws['B7'] = newList[2]['tipo']
        ws['C7'] = newList[2]['total']
        if newList[2]['tipo'] == listaOrdenada[8]['tipo']:
            B7 = ws['B7']
            C7 = ws['C7']
            ft = Font(bold=True)
            B7.font = ft
            C7.font = ft
            ws['B7'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
            ws['C7'].fill = PatternFill(bgColor="d9d9d9", fill_type = "lightGray")
        ws['B8'] = newList[3]['tipo']
        ws['C8'] = newList[3]['total']
        if newList[3]['tipo'] == listaOrdenada[8]['tipo']:
            B8 = ws['B8']
            C8 = ws['C8']
            ft = Font(bold=True)
            B8.font = ft
            C8.font = ft
            ws['B8'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C8'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['B9'] = newList[4]['tipo']
        ws['C9'] = newList[4]['total']
        if newList[4]['tipo'] == listaOrdenada[8]['tipo']:
            B9 = ws['B9']
            C9 = ws['C9']
            ft = Font(bold=True)
            B9.font = ft
            C9.font = ft
            ws['B9'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C9'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['B10'] = newList[5]['tipo']
        ws['C10'] = newList[5]['total']
        if newList[5]['tipo'] == listaOrdenada[8]['tipo']:
            B10 = ws['B10']
            C10 = ws['C10']
            ft = Font(bold=True)
            B10.font = ft
            C10.font = ft
            ws['B10'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C10'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['B11'] = newList[6]['tipo']
        ws['C11'] = newList[6]['total']
        if newList[6]['tipo'] == listaOrdenada[8]['tipo']:
            B11 = ws['B11']
            C11 = ws['C11']
            ft = Font(bold=True)
            B11.font = ft
            C11.font = ft
            ws['B11'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C11'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['B12'] = newList[7]['tipo']
        ws['C12'] = newList[7]['total']
        if newList[7]['tipo'] == listaOrdenada[8]['tipo']:
            B12 = ws['B12']
            C12 = ws['C12']
            ft = Font(bold=True)
            B12.font = ft
            C12.font = ft
            ws['B12'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C12'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['B13'] = newList[8]['tipo']
        ws['C13'] = newList[8]['total']
        if newList[8]['tipo'] == listaOrdenada[8]['tipo']:
            B13 = ws['B13']
            C13 = ws['C13']
            ft = Font(bold=True)
            B13.font = ft
            C13.font = ft
            ws['B13'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
            ws['C13'].fill = PatternFill(bgColor="D9D9D9", fill_type = "lightGray")
        ws['O21'] = evaluacion.get_centroPrimario_display()
        ws['O22'] = evaluacion.get_centroSecundario_display()
        ws['O23'] = evaluacion.get_centroTerciario_display()
        ws['N25'] = centro.descripcion
        ws['B21'] = eneatipoPrincipal.descripcion
        ws['B30'] = eneatipoSecundario.descripcion
        ws['B39'] = eneatipoTerciario.descripcion
        if evaluacion.centroPrimario == '1':
            ws['Q21'] = evaluacion.centroEmocional
        elif evaluacion.centroPrimario == '2':
            ws['Q21'] = evaluacion.centroFisico
        elif evaluacion.centroPrimario == '3':
            ws['Q21'] = evaluacion.centroIntelectual
        if evaluacion.centroSecundario == '1':
            ws['Q22'] = evaluacion.centroEmocional
        elif evaluacion.centroSecundario == '2':
            ws['Q22'] = evaluacion.centroFisico
        elif evaluacion.centroSecundario == '3':
            ws['Q22'] = evaluacion.centroIntelectual
        if evaluacion.centroTerciario == '1':
            ws['Q23'] = evaluacion.centroEmocional
        elif evaluacion.centroTerciario == '2':
            ws['Q23'] = evaluacion.centroFisico
        elif evaluacion.centroTerciario == '3':
            ws['Q23'] = evaluacion.centroIntelectual
        ws['B20'] = listaOrdenada[8]['tipo']
        ws['B29'] = listaOrdenada[7]['tipo']
        ws['B38'] = listaOrdenada[6]['tipo']

        ws['K7'] = listaOrdenada[8]['tipo']
        ws['L7'] = listaOrdenada[8]['total']
        ws['K8'] = listaOrdenada[7]['tipo']
        ws['L8'] = listaOrdenada[7]['total']
        ws['K9'] = listaOrdenada[6]['tipo']
        ws['L9'] = listaOrdenada[6]['total']

        ws['O34'] = evaluacion.get_energiaPrimaria_display()
        ws['O35'] = evaluacion.get_energiaSecundaria_display()
        ws['O36'] = evaluacion.get_energiaTerciaria_display()
        ws['N38'] = energia.descripcion

        if evaluacion.energiaPrimaria == '1':
            ws['Q34'] = evaluacion.energiaInterna
        elif evaluacion.energiaPrimaria == '2':
            ws['Q34'] = evaluacion.energiaExterna
        elif evaluacion.energiaPrimaria == '3':
            ws['Q34'] = evaluacion.energiaEquilibrio
        if evaluacion.energiaSecundaria == '1':
            ws['Q35'] = evaluacion.energiaInterna
        elif evaluacion.energiaSecundaria == '2':
            ws['Q35'] = evaluacion.energiaExterna
        elif evaluacion.energiaSecundaria == '3':
            ws['Q35'] = evaluacion.energiaEquilibrio
        if evaluacion.energiaTerciaria == '1':
            ws['Q36'] = evaluacion.centroEmocional
        elif evaluacion.energiaTerciaria == '2':
            ws['Q36'] = evaluacion.energiaExterna
        elif evaluacion.energiaTerciaria == '3':
            ws['Q36'] = evaluacion.energiaEquilibrio

        img = Image(settings.MEDIA_ROOT + '/excel/LOGO_EXCEL.png')
        ws.add_image(img,'R50')

        nombre_archivo = "Reporte_Eneagrama {0} {1}.xlsx".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos)
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        workbook = wb
        output = BytesIO()
        workbook.save(output)

        subject = 'Eneagrama, resultados para: {0}'.format(evaluacion.usuario.nombre)
        html_content = get_template('eneagrama/email/formato_email.html').render({'evaluacion': evaluacion})

        msg = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['manuel.chavez.carrillo@gmail.com',],
            cc=['c.iturriosalcaraz@gmail.com',],
        )
        msg.content_subtype = "html"
        msg.attach("Reporte Eneagrama {0} {1}.xlsx".format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos), output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        msg.send(fail_silently= not settings.DEBUG)
        messages.success(request, '¡{0} {1}, Tu reporte te llegara a tu correo en unos momentos!'.format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        return redirect('Eneagrama:principal')


def principal(request):
    return render(request, 'eneagrama/principal.html')


def register(request):
    if 'nombre' in request.session:
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
        messages.success(request, '¡Bienvenido de nuevo {0} {1}!'.format(evaluacion.usuario.nombre, evaluacion.usuario.apellidos))
        return redirect('Eneagrama:parteUno')
    nombreMostrar = None
    if request.method == "POST":
        nombre = request.POST.get('nombre', None)
        apellidos = request.POST.get('apellidos', None)
        email = request.POST.get('email', None)
        edad = request.POST.get('edad', None)
        empresa = request.POST.get('empresa', None)
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
            check_email.pais = pais
            check_email.estado = estado
            check_email.ciudad = ciudad
            check_email.save()
            request.session['nombre'] = nombre
            evaluacion = Evaluacion.objects.get(usuario=check_email)
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
            return redirect('Eneagrama:parteUno')
        else:
            messages.warning(request, 'Contacta al administrador para que puedas iniciarlizar en la aplicación.')
            return redirect('Eneagrama:register')

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
        messages.success(request, '¡Enhorabuena has compleatado la evaluacion con exito!')
        return redirect('Eneagrama:pago_formato')

    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/perfil_de_personalidad_parte_7.html', {'nombreMostrar': nombreMostrar})


def pago_formato(request):
    if not 'nombre' in request.session:
        messages.warning(request, '¡Antes de obtener tu formato debes de identificarte!')
        return redirect('Eneagrama:register')
    else:
        evaluacion = Evaluacion.objects.get(id=request.session['id_evaluacion'])
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
    nombreMostrar = request.session['nombre']
    return render(request, 'eneagrama/pago_formato.html', {'nombreMostrar': nombreMostrar, 'evaluacion': evaluacion})


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
        del request.session['nombre']
        del request.session['id_evaluacion']
        return redirect('Eneagrama:register')