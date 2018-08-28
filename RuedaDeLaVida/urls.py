# -*- coding: utf-8 -*-
"""
RuedaDeLaVida URL Configuration
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    # Redirect / to WebPagRuedaDLV
    url(r'^$', RedirectView.as_view(url='rueda-de-la-vida/'), name='index'),

    # URLs sitio administracion
    url(r'^admin/', admin.site.urls),

    # Urls login
    url(r'^rueda-de-la-vida/', include('django.contrib.auth.urls')),

    # URLs Eneagrama
    url(r'^eneagrama/', include('Eneagrama.urls', namespace='Eneagrama')),

    # URLs WebPagRuedaDLV
    url(r'^rueda-de-la-vida/', include('WebPagRuedaDLV.urls', namespace='WebPagRuedaDLV')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
