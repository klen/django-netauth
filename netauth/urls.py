from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import direct_to_template

from netauth import views


urlpatterns = patterns('',
    url(r'^begin/(\w+)/$', views.begin, name='netauth-begin'),
    url(r'^complete/(\w+)/$', views.complete, name='netauth-complete'),
    url(r'^extra/(\w+)/$', views.extra, name='netauth-extra'),
    url(r'^login/$', direct_to_template, {'template': 'netauth/login.html'}, name='netauth-login'),
    url(r'^logout/$', views.logout, name='netauth-logout'),

    url(r'^ya_proxy/$', direct_to_template, {'template': 'netauth/yandex_proxy.html'}, name='netauth-yandex-proxy'),
)
