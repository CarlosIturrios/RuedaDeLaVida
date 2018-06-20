from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^finanzas-dinero/$', views.finanzas_dinero, name='finanzas_dinero'),
   	url(r'^salud-vitalidad/$', views.salud_vitalidad, name='salud_vitalidad'),
   	url(r'^familia_amigos/$', views.familia_amigos, name='familia_amigos'),
   	url(r'^amor-relaciones/$', views.amor_relaciones, name='amor_relaciones'),
   	url(r'^crecimiento-personal-aprendizaje/$', views.crecimiento_personal_aprendizaje, name='crecimiento_personal_aprendizaje'),
   	url(r'^diversion-estilo-de-vida/$', views.diversion_estilo_de_vida, name='diversion_estilo_de_vida'),
   	url(r'^productividad-personal/$', views.productividad_personal, name='productividad_personal'),
   	url(r'^register/$', views.register, name='register'),
   	url(r'^resultados/$', views.resultados, name='resultados'),
    url(r'^slider/$', views.slider, name='slider'),

]