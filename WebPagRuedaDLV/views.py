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
from django.contrib.auth.models import User, Group
from django.conf import settings

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
	return render(request, 'principal.html')


def psicologica(request):
	print(request.session['wheel'])	
	if request.method == "POST":
		slide3 = int(request.POST.get('slide3', None))
		slide4 = int(request.POST.get('slide4', None))
		text3 = request.POST.get('text3', None)
		text4 = request.POST.get('text4', None)
		if slide3 < slide4:
			request.session['wheel']['slide3'] = slide3
			request.session['wheel']['slide4'] = slide4
			request.session['wheel']['text3'] = text3
			request.session['wheel']['text4'] = text4
			print(request.session['wheel'])
			return redirect('WebPagRuedaDLV:relacionesAmor')
	return render(request, 'psicologica.html')


def relacionesAmor(request):
	print(request.session['wheel'])
	if request.method == "POST":
		slide5 = int(request.POST.get('slide5', None))
		slide6 = int(request.POST.get('slide6', None))
		text5 = request.POST.get('text5', None)
		text6 = request.POST.get('text6', None)
		if slide5 < slide6:
			request.session['wheel']['slide5'] = slide5
			request.session['wheel']['slide6'] = slide6
			request.session['wheel']['text5'] = text5
			request.session['wheel']['text6'] = text6
			return redirect('WebPagRuedaDLV:productividadPersonal')
	return render(request, 'relacionesAmor.html') 


def productividadPersonal(request):
	return render(request, 'productividadPersonal.html')


def register(request):
	if request.method == "POST":		
		nombre = request.POST.get('username', None)
		apellidos = request.POST.get('lasname', None)
		email = request.POST.get('email', None)
		correo = Correo()
		correo.nombre = nombre
		correo.apellidos = apellidos
		correo.correo = email
		correo.save()
		return redirect('WebPagRuedaDLV:resultados')
	return render(request, 'register.html')


def resultados(request):
	return render(request, 'resultados.html')