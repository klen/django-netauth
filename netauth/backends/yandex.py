from netauth.backends import OAuthBaseBackend
import ipdb as pdb
from netauth.exceptions import Redirect
from django.conf import settings
from django.core.serializers import xml_serializer

class YandexBackend( OAuthBaseBackend ):

    APPLICATION_ID = property(lambda self: getattr(settings, "%s_APPLICATION_ID" % self.provider.upper()))

    def begin( self, request, data ):
        request = self.get_request( url= self.AUTHORIZE_URL , parameters = { 'client_id': self.APPLICATION_ID, 'response_type': 'token' })
        raise Redirect(request.to_url())

    def validate( self, request, data ):
        try:
            self.identity = data['access_token']
        except KeyError:
            self.error(request)

    def get_extra_data(self, response):
        request = self.get_request( url=self.API_URL, parameters = { 'oauth_token': self.identity })
        content = self.load_request( request )
        xml_serializer.Deserializer( content )
        pdb.set_trace() ############################## XXX Breakpoint ##############################
