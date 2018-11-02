# -*- coding: utf-8 -*-
"""
Django settings for RuedaDeLaVida project.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# APP CONFIG
SITE_ID = 1

DEBUG = True

SECRET_KEY = 'mv9z(m^8@g5f--t8-2gmjvcwlh%4pzo^g=exmb73bxat$eh+=f'

ALLOWED_HOSTS = []

ROOT_URLCONF = 'RuedaDeLaVida.urls'

WSGI_APPLICATION = 'RuedaDeLaVida.wsgi.application'

DEFAULT_CHARSET = 'utf-8'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'mathfilters',
    'WebPagRuedaDLV',
    'Eneagrama',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# LOCALIZATION
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Hermosillo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# FILES
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# AUTHENTICATION
LOGIN_URL = '/rueda-de-la-vida/login/'

LOGIN_REDIRECT_URL = '/rueda-de-la-vida/resultados/'

LOGOUT_REDIRECT_URL = '/evaluacion-eneagrama/'
#LOGOUT_REDIRECT_URL = None

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# SESSION
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 1209600  # 2 Weeks


try:
    from local_settings import *
except ImportError:
    pass
