from __future__ import absolute_import
try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new

import urlparse

from django.contrib import messages
from django.conf import settings

from publicauth.backends import BaseBackend
from public.exceptions import Redirect
from publicauth import lang


class VkontakteBackend(BaseBackend):

    def validate(self, request, data):
        cookie_name = "vk_app_%s" % settings.VKONTAKTE_APP_ID
        try:
            cookie_data = urlparse.parse_qs(request.COOKIES[cookie_name])
            value = ""
            for i in ('expire', 'mid', 'secret', 'sid'):
                value += "%s=%s" % (i, cookie_data[i][0] )
            if cookie_data['sig'][0] == md5(value + settings.VKONTAKTE_SECRET_KEY).hexdigest():
                self.identity = cookie_data['mid'][0]
            else:
                raise ValueError()
        except (KeyError, IndexError, AttributeError, ValueError):
            messages.error(request, lang.VKONTAKTE_INVALID_RESPONSE)
            raise Redirect('publicauth-login')

    def complete(self, request, response):
        request.session['next_url'] = request.GET.get("next") or settings.LOGIN_REDIRECT_URL
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        raise Redirect('publicauth-extra', 'vkontakte')

    def get_extra_data(self, response):
        return {}
