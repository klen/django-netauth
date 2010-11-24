from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse

from oauth2 import Request

from publicauth.exceptions import Redirect
from publicauth.backends import BaseBackend
from publicauth import lang


class FacebookBackend(BaseBackend):

    APP_ID = property(lambda self: getattr(settings, "%s_APP_ID" % self.provider.upper()))
    AUTHORIZE_URL = property(lambda self: getattr(settings, "%s_AUTHORIZE_URL" % self.provider.upper()))

    def begin( self, request, data ):
        request = Request( self.AUTHORIZE_URL, parameters = {
            'client_id' : self.APP_ID,
            'redirect_uri' : request.build_absolute_uri(reverse('publicauth-complete', args=[self.provider])),
        })
        raise Redirect(request.to_url())

    def validate(self, request, data):
        if not request.facebook.validate_cookie_signature(request.COOKIES):
            messages.error(request, lang.FACEBOOK_INVALID_RESPONSE)
            raise Redirect('publicauth-login')
        else:
            uid = request.facebook.api_key
            self.identity = request.COOKIES.get('%s_user' % uid)
            return request.facebook

    def complete(self, request, response):
        request.session['next_url'] = request.GET.get("next") or settings.LOGIN_REDIRECT_URL
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        raise Redirect('publicauth-extra', 'facebook')

    def get_extra_data(self, response):
        extra_fields = [i for i in self.PROFILE_MAPPING]
        return response.users.getInfo([self.identity], extra_fields)[0]

    def get_url( self, http_url=None, parameters=dict() ):
        pass

