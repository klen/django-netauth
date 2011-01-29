from xml.etree.ElementTree import fromstring

from netauth import RedirectException, settings
from netauth.backends import OAuthBaseBackend


class YandexBackend( OAuthBaseBackend ):

    APPLICATION_ID = property(lambda self: getattr(settings, "%s_APPLICATION_ID" % self.provider.upper()))

    def begin( self, request, data ):
        request = self.get_request( url= self.AUTHORIZE_URL , parameters = { 'client_id': self.APPLICATION_ID, 'response_type': 'token' })
        raise RedirectException(request.to_url())

    def validate( self, request, data ):
        try:
            self.identity = data['access_token']
        except KeyError:
            self.error(request)
        request = self.get_request(url=self.API_URL, parameters = { 'oauth_token': self.identity })
        return self.load_request(request)

    def get_extra_data(self, response):
        tree = fromstring(response)
        namespace = '{http://api.yandex.ru/yaru/}'
        fields = ['name', 'email', 'city', 'country', 'sex', 'mobile_phone', 'metro']
        result = dict()
        for name in fields:
            value = tree.find( "%s%s" % ( namespace, name ))
            result[ name ] = value.text
        return result
