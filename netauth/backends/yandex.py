from netauth.backends import OAuthBaseBackend
from netauth.exceptions import Redirect
from django.conf import settings

class YandexBackend( OAuthBaseBackend ):

    APPLICATION_ID = property(lambda self: getattr(settings, "%s_APPLICATION_ID" % self.provider.upper()))

    def begin( self, request, data ):
        request = self.get_request( url= self.AUTHORIZE_URL , parameters = { 'client_id': self.APPLICATION_ID, 'response_type': 'token' })
        raise Redirect(request.to_url())

    def validate( self, request, data ):
        pass

    def complite( self, request, data ):
        pass
