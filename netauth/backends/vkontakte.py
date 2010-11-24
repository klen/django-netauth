import urlparse

from django.conf import settings

from netauth.backends import BaseBackend


try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new





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
            self.error(request)

