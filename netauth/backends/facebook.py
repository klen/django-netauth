from django.conf import settings

from netauth.backends import OAuthBaseBackend
from netauth.exceptions import Redirect


class FacebookBackend(OAuthBaseBackend):

    APPLICATION_ID = property(lambda self: getattr(settings, "%s_APPLICATION_ID" % self.provider.upper()))
    APPLICATION_SECRET = property(lambda self: getattr(settings, "%s_APPLICATION_SECRET" % self.provider.upper()))

    def begin( self, request, data ):
        request = self.get_request( url=self.AUTHORIZE_URL, parameters = {
            'client_id' : self.APPLICATION_ID,
            'redirect_uri' : self.callback(request),
        })
        raise Redirect(request.to_url())

    def validate(self, request, data):

        from netauth import log
        log.info( 'start validate' )
        if not data.get('code'):
            self.error(request)

        log.info( 'create request' )
        request = self.get_request( url=self.ACCESS_TOKEN_URL, parameters = {
            'client_id' : self.APPLICATION_ID,
            'client_secret': self.APPLICATION_SECRET,
            'code': data['code']
        })

        content = self.load_request(request)
        self.identity = self.parse_qs(content)['access_token'][0]
        return content

    def get_extra_data(self, response):

        extra_fields = [i for i in self.PROFILE_MAPPING]
        return response.users.getInfo([self.identity], extra_fields)[0]
