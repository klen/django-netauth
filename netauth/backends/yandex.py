from xml.etree.ElementTree import fromstring

from django.conf import settings

from netauth.backends import OAuthBaseBackend
from netauth.exceptions import Redirect


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
        tree = fromstring(content)
        namespace = '{http://api.yandex.ru/yaru/}'
        fields = [ 'name', 'email', 'city', 'country' ]
        result = dict()
        for name in fields:
            value = tree.find( "%s%s" % ( namespace, name ))
            result[ name ] = value.text
        return result
