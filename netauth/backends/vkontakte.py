from django.conf import settings

from netauth.backends import OAuthBaseBackend
from netauth import log


try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new


class VkontakteBackend(OAuthBaseBackend):

    def validate(self, request, data):
        cookie_name = "vk_app_%s" % settings.VKONTAKTE_APPLICATION_ID
        try:
            cookie_data = self.parse_qs(request.COOKIES[cookie_name])
            value = ""
            for i in ('expire', 'mid', 'secret', 'sid'):
                value += "%s=%s" % (i, cookie_data[i][0] )
            if cookie_data['sig'][0] == md5(value + settings.VKONTAKTE_APPLICATION_SECRET).hexdigest():
                self.identity = cookie_data['mid'][0]
            else:
                raise ValueError()
        except (KeyError, IndexError, AttributeError, ValueError):
            log.info(value)
            log.info(cookie_data['sig'][0])
            log.info(md5(value + settings.VKONTAKTE_APPLICATION_SECRET).hexdigest())
            self.error(request)
        return data

    def get_extra_data(self, response):
        return self.parse_qs(response)
