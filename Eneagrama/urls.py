from django.conf.urls import url, include

from . import views
from .views import Borrar_sesion

urlpatterns = [
    url(r'^$', views.principal, name='principal'),
    url(r'^taller/$', views.taller, name='taller'),
    url(r'^register/(?P<metodo_pago>[0-9]+)/$', views.register, name='register'),
    url(r'^perfil-de-personalidad-parte-1/$', views.parteUno, name='parteUno'),
    url(r'^perfil-de-personalidad-parte-2/$', views.parteDos, name='parteDos'),
    url(r'^perfil-de-personalidad-parte-3/$', views.parteTres, name='parteTres'),
    url(r'^perfil-de-personalidad-parte-4/$', views.parteCuatro, name='parteCuatro'),
    url(r'^perfil-de-personalidad-parte-5/$', views.parteCinco, name='parteCinco'),
    url(r'^perfil-de-personalidad-parte-6/$', views.parteSeis, name='parteSeis'),
    url(r'^perfil-de-personalidad-parte-7/$', views.parteSiete, name='parteSiete'),
    url(r'^pago-formato/$', views.pago_formato, name='pago_formato'),
    url(r'^obtencion-de-valores/$', views.obtencion_de_valores, name='obtencion_de_valores'),
    url(r'^borrar-sesion/$', Borrar_sesion.as_view(), name="borrar_sesion"),
    url(r'^metodo-pago/$', views.metodo_pago, name='metodo_pago'),
    url(r'^realizar-pago/$', views.realizar_pago, name='realizar_pago'),
    url(r'^registrar-comprobante/$', views.registrar_comprobante, name='registrar_comprobante'),
    url(r'^reporte-Eneagrama/$', views.Reporte_eneagrama, name="Reporte_eneagrama"),
    url(r'^reporte-en-pdf-Eneagrama/(?P<pk>[0-9]+)/$', views.write_pdf_view, name='write_pdf_view'),
    url(r'^dashboard/$', views.Dashboard, name="Dashboard"),
    url(r'^modificar-codigo/(?P<pk>[0-9]+)/$', views.Modificar_codigo, name='Modificar_codigo'),
    url(r'^crear-codigo/$', views.Crear_codigo, name='Crear_codigo'),
    url(r'^comprobante-deposito/(?P<pk>[0-9]+)/$', views.Comprobante_deposito, name='Comprobante_deposito'),
    url(r'^paypal-standard-ipn-urls/', include('paypal.standard.ipn.urls')),
]
