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
            access_token = data['access_token']
            request = self.get_request(url=self.API_URL, parameters = { 'oauth_token': access_token })
            content = self.load_request(request)
            xml = fromstring(content)
            extra = dict(
                (name, xml.find("{http://api.yandex.ru/yaru/}%s" % name).text)
                for name in ['id', 'name', 'email', 'city', 'country', 'sex', 'mobile_phone', 'metro']
            )
            self.identity = extra['id']
        except KeyError:
            self.error(request)

        return extra

    def get_extra_data(self, response):
        return response
