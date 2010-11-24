from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from publicauth import views


urlpatterns = patterns('',
    url(r'^begin/(\w+)/$', views.begin, name='publicauth-begin'),
    url(r'^complete/(\w+)/$', views.complete, name='publicauth-complete'),
    url(r'^extra/(\w+)/$', views.extra, name='publicauth-extra'),
    url(r'^login/$', direct_to_template, {'template': 'publicauth/login.html'}, name='publicauth-login'),
    url(r'^facebook-xdreceiver/$', direct_to_template, {'template': 'publicauth/facebook-xdreceiver.html'}, name='publicauth-facebook-xdreceiver'),
    url(r'^vkontakte-xdreceiver/$', direct_to_template, {'template': 'publicauth/vkontakte-xdreceiver.html'}, name='publicauth-vkontakte-xdreceiver'),
    url(r'^logout/$', views.logout, name='publicauth-logout'),
)
