from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^psicologica/$', views.psicologica, name='psicologica'),
   	url(r'^relacionesAmor/$', views.relacionesAmor, name='relacionesAmor'),
   	url(r'^productividadPersonal/$', views.productividadPersonal, name='productividadPersonal'),
   	url(r'^register/$', views.register, name='register'),
   	url(r'^resultados/$', views.resultados, name='resultados'),
    url(r'^slider/$', views.slider, name='slider'),

]