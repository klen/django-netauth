from django.conf import settings

from netauth.backends import OAuthBaseBackend


try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new


class VkontakteBackend(OAuthBaseBackend):

    def validate(self, request, data):
        cookie_name = "vk_app_%s" % settings.VKONTAKTE_APPLICATION_ID
        try:
            content = request.COOKIES[cookie_name]
            cookie_data = self.parse_qs(content)
            value = ""
            for i in ('expire', 'mid', 'secret', 'sid'):
                value += "%s=%s" % (i, cookie_data[i][0] )
            if cookie_data['sig'][0] == md5(value + settings.VKONTAKTE_APPLICATION_SECRET).hexdigest():
                self.identity = cookie_data['mid'][0]
            else:
                raise ValueError()
        except (KeyError, IndexError, AttributeError, ValueError):
            self.error(request)
        return content

    def get_extra_data(self, response):
        return self.parse_qs(response)
