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

        url = request.to_url()

        raise RedirectException(url)

    def validate(self, request, data):

        if not data.get('code'):
            self.error(request)

        # Get token
        request = self.get_request( url=self.ACCESS_TOKEN_URL, parameters = {
            'client_id' : self.APPLICATION_ID,
            'redirect_uri' : self.get_callback(request),
            'client_secret': self.APPLICATION_SECRET,
            'code': data['code'],
        })
        content = self.load_request(request)
        access_token = self.parse_qs(content)['access_token'][0]

        # Get user info
        request = self.get_request( url=self.API_URL, parameters = { 'access_token': access_token })
        extra = simplejson.loads(self.load_request(request))
        try:
            self.identity = extra['id']
        except KeyError:
            self.error(request)
        return extra

    def get_extra_data(self, response):
        return response
