# -*- coding: utf-8 -*-
"""
RuedaDeLaVida URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include, handler404
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    # URLs Eneagrama
    url(r'^evaluacion-eneagrama/', include('Eneagrama.urls', namespace='Eneagrama')),

    # URLs WebPagRuedaDLV
    url(r'^rueda-de-la-vida/', include('WebPagRuedaDLV.urls', namespace='WebPagRuedaDLV')),

    # Urls login
    url(r'^auth/', include('django.contrib.auth.urls')),

    # URLs sitio administracion
    url(r'^admin/', admin.site.urls),

    # Redirect / to WebPagRuedaDLV
    url(r'^', include('landingpage.urls'), name='landingpage'),
]

handler404 = 'Eneagrama.views.error_404_view'

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
