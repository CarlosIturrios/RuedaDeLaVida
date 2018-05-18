from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    
    # Auth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/WebPagRuedaDLV/login/'}, name='logout'),

    # App views    
   	url(r'^$', views.principal, name='principal'),
   	
]