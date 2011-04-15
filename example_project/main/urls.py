from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.views.defaults import page_not_found, server_error

import main.views as mainviews


# 404 and 500 handlers
handler404 = page_not_found
handler500 = server_error

# Project urls
urlpatterns = patterns( '',
    url('^$', mainviews.index, name='index'),
    url('^accounts/profile/$', mainviews.profile, name='profile'),
    url('^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # Net auth
    url('^auth/', include('netauth.urls')),
)

# Django admin
admin.autodiscover()
urlpatterns += [ url(r'^admin/', include(admin.site.urls)), ]

# Serve static in dev mode
urlpatterns += url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

