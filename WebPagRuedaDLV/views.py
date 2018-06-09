# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse #email sender
from django.template import Context #email sender
from django.template.loader import render_to_string, get_template #email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives #email sender
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.conf import settings

from decimal import Decimal 
from datetime import datetime
from .models import Correo, Respuesta
# Create your views here.
def principal(request):	
	if request.method == "POST":
		slide1 = int(request.POST.get('slide1', None))
		slide2 = int(request.POST.get('slide2', None))
		text1 = request.POST.get('text1', None)
		text2 = request.POST.get('text2', None)
		if slide1 < slide2:
			request.session['wheel'] = {'slide1': slide1, 'slide2': slide2, 'text1':text1, 'text2':text2}
			return redirect('WebPagRuedaDLV:psicologica')
		else:
			messages.success(request, 'El primer controlador tiene que ser mayor al segundo!') 
	return render(request, 'principal.html')


def psicologica(request):
	print(request.session['wheel'])	
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
			print(request.session['wheel'])
			return redirect('WebPagRuedaDLV:relacionesAmor')
	return render(request, 'psicologica.html')


def relacionesAmor(request):
	print(request.session['wheel']['slide4'])
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
			return redirect('WebPagRuedaDLV:productividadPersonal')
	return render(request, 'relacionesAmor.html') 


def productividadPersonal(request):
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
	return render(request, 'productividadPersonal.html')


def register(request):
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
	salud = float(slide1) / float(slide2)
	salud = (1-(salud))*100
	salud = int(salud)
	slide3 = request.session['wheel']['slide3']
	slide4 = request.session['wheel']['slide4']
	psicologica = float(slide3) / float(slide4)
	psicologica = (1-(psicologica))*100
	psicologica = int(psicologica)
	slide5 = request.session['wheel']['slide5']
	slide6 = request.session['wheel']['slide6']
	relaciones = float(slide5) / float(slide6)
	relaciones = (1-(relaciones))*100
	relaciones = int(relaciones)
	gap1 = slide1+slide3+slide5
	gap2 = slide2+slide4+slide6
	gaptotal = float(gap1)/float(gap2)
	gaptotal = (1-(gaptotal))*100
	gaptotal = int(gaptotal) 
	return render(request, 'resultados.html', {'slide1':slide1, 'slide2':slide2, 'salud':salud, 'slide3':slide3, 'slide4':slide4, 'psicologica':psicologica, 'slide5':slide5, 'slide6':slide6, 'relaciones':relaciones, 'gaptotal':gaptotal })


def slider(request):
	messages.success(request, 'Your password was updated successfully!') 
	return render(request,'slider.html')	
