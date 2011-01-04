from netauth import settings
from netauth.backends import OAuthBaseBackend

try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new

class VkontakteBackend(OAuthBaseBackend):

    def validate(self, request, data):
        try:
            content = request.COOKIES[ "vk_app_%s" % settings.VKONTAKTE_APPLICATION_ID ]
            cd = self.parse_qs(content)
            value = ''.join(["%s=%s" % (i, cd[i][-1]) for i in ('expire', 'mid', 'secret', 'sid')])
            if cd['sig'][-1] == md5(value + settings.VKONTAKTE_APPLICATION_SECRET).hexdigest():
                self.identity = cd['mid'][-1]
            else:
                raise ValueError
        except ( KeyError, ValueError ):
            self.error(request)
        self.data = data
        return content

    def get_extra_data(self, response):
        result = {}
        for vk_field, field in settings.VKONTAKTE_PROFILE_MAPPING.items():
            result[field] = self.data[vk_field]
        return result
