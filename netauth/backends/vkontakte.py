from django.conf import settings

from netauth.backends import OAuthBaseBackend


try:
    from hashlib import md5
except ImportError:
    import md5
    md5 = md5.new


class VkontakteBackend(OAuthBaseBackend):

    def validate(self, request, data):
        try:
            sig = data['hash']
            safe_sig = "%s%s%s" % ( settings.VKONTAKTE_APPLICATION_ID, data['uid'], settings.VKONTAKTE_APPLICATION_SECRET )
            safe_sig = md5(safe_sig).hexdigest()
        except KeyError:
            self.error(request)

        if sig == safe_sig:
            self.identity = data['uid']
        else:
            self.error(request)

        return data

    def get_extra_data(self, response):
        return response
