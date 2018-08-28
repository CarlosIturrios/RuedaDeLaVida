from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # App views    
   	url(r'^$', views.principal, name='principal'),
    url(r'^register/$', views.register, name='register'),
    url(r'^perfil-de-personalidad-parte-1/$', views.parteUno, name='parteUno'),
    url(r'^perfil-de-personalidad-parte-2/$', views.parteDos, name='parteDos'),
    url(r'^perfil-de-personalidad-parte-3/$', views.parteTres, name='parteTres'),
    url(r'^perfil-de-personalidad-parte-4/$', views.parteCuatro, name='parteCuatro'),
    url(r'^perfil-de-personalidad-parte-5/$', views.parteCinco, name='parteCinco'),
    url(r'^perfil-de-personalidad-parte-6/$', views.parteSeis, name='parteSeis'),
    url(r'^perfil-de-personalidad-parte-7/$', views.parteSiete, name='parteSiete'),
]