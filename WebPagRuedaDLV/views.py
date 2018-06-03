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

# Create your views here.
def principal(request):
	return render(request, 'principal.html')


def psicologica(request):
	return render(request, 'psicologica.html')


def relacionesAmor(request):
	return render(request, 'relacionesAmor.html')


def productividadPersonal(request):
	return render(request, 'productividadPersonal.html')


def register(request):
	return render(request, 'register.html')


def resultados(request):
	return render(request, 'resultados.html')