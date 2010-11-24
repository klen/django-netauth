from django.contrib import messages
from django.conf import settings

from publicauth.exceptions import Redirect
from publicauth.backends import BaseBackend
from publicauth import lang


class FacebookBackend(BaseBackend):

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

