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
    url(r'^$', RedirectView.as_view(url='WebPagRuedaDLV/'), name='index'),

    # URLs sitio administracion
    url(r'^admin/', admin.site.urls),

    # URLs allauth
    url(r'^allauth/',include('allauth.urls')),

    # URLs WebPagRuedaDLV
    url(r'^WebPagRuedaDLV/', include('WebPagRuedaDLV.urls', namespace='WebPagRuedaDLV'))
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
