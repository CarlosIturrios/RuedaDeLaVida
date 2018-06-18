from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^finanzas_dinero/$', views.finanzas_dinero, name='finanzas_dinero'),
   	url(r'^salud_vitalidad/$', views.salud_vitalidad, name='salud_vitalidad'),
   	url(r'^familia_amigos/$', views.familia_amigos, name='familia_amigos'),
   	url(r'^register/$', views.register, name='register'),
   	url(r'^resultados/$', views.resultados, name='resultados'),
    url(r'^slider/$', views.slider, name='slider'),

]