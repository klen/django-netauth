from django.utils import simplejson

from netauth import settings, RedirectException
from netauth.backends import OAuthBaseBackend


class FacebookBackend(OAuthBaseBackend):

    APPLICATION_ID = property(lambda self: getattr(settings, "%s_APPLICATION_ID" % self.provider.upper()))
    APPLICATION_SECRET = property(lambda self: getattr(settings, "%s_APPLICATION_SECRET" % self.provider.upper()))

    def begin( self, request, data ):
        request = self.get_request( url=self.AUTHORIZE_URL, parameters = {
            'client_id' : self.APPLICATION_ID,
            'redirect_uri' : self.get_callback(request),
        })
        raise RedirectException(request.to_url())

    def validate(self, request, data):

        if not data.get('code'):
            self.error(request)

        request = self.get_request( url=self.ACCESS_TOKEN_URL, parameters = {
            'client_id' : self.APPLICATION_ID,
            'redirect_uri' : self.get_callback(request),
            'client_secret': self.APPLICATION_SECRET,
            'code': data['code'],
        })
        content = self.load_request(request)
        self.identity = self.parse_qs(content)['access_token'][0]
        return content

    def get_extra_data(self, response):
        request = self.get_request( url=self.API_URL, parameters = { 'access_token': self.identity })
        content = self.load_request(request)
        return simplejson.loads(content)
