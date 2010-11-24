from __future__ import absolute_import

import httplib2
import urlparse

from oauth2 import Consumer, Token, Request, SignatureMethod_HMAC_SHA1

from django.conf import settings as global_settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib import messages

from publicauth import log
from publicauth.exceptions import Redirect
from publicauth.backends import BaseBackend
from publicauth import lang


class OAuthError( Exception ):
    pass


class OAuthBackend(BaseBackend):

    CONSUMER_KEY = property(lambda self: getattr(global_settings, "%s_CONSUMER_KEY" % self.provider.upper()))
    CONSUMER_SECRET = property(lambda self: getattr(global_settings, "%s_CONSUMER_SECRET" % self.provider.upper()))
    REQUEST_TOKEN_URL = property(lambda self: getattr(global_settings, "%s_REQUEST_TOKEN_URL" % self.provider.upper()))

    ACCESS_TOKEN_URL = property(lambda self: getattr(global_settings, "%s_ACCESS_TOKEN_URL" % self.provider.upper()))
    AUTHORIZE_URL = property(lambda self: getattr(global_settings, "%s_AUTHORIZE_URL" % self.provider.upper()))
    API_URL = property(lambda self: getattr(global_settings, "%s_API_URL" % self.provider.upper()))

    def __init__( self, *args, **kwargs ):
        super( OAuthBackend, self ).__init__( *args, **kwargs )
        self.consumer = Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.signature_method = SignatureMethod_HMAC_SHA1()

    def begin(self, request, data):
        """ Try to get Request Token from OAuth Provider and
            redirect user to provider's site for approval.
        """
        # callback = request.build_absolute_uri(reverse('publicauth-complete', args=[self.provider]))
        url = self.__get_url( http_url=self.REQUEST_TOKEN_URL )

        response, content = httplib2.Http().request(url)

        if response[ 'status' ] != 200:
            log.info(content)
            raise OAuthError( "No access to private resources.")

        url = self.__get_url( token = Token.from_string( content ), http_url=self.AUTHORIZE_URL,)
        raise Redirect(url)

    def validate(self, request, data):
        try:
            parameters = dict(
                    oauth_token = data['oauth_token'],
                    oauth_verifier = data.get('oauth_verifier', None))
        except MultiValueDictKeyError:
            messages.error(request, lang.BACKEND_ERROR)
            raise Redirect('publicauth-login')

        url = self.__get_url( http_url=self.ACCESS_TOKEN_URL, parameters=parameters)
        response, content = httplib2.Http().request(url)

        if response[ 'status' ] != 200:
            raise OAuthError( "No access to private resources.")

        self.identity = urlparse.parse_qs(content, keep_blank_values=False)['oauth_token'][0]
        return content

    def complete(self, request, response):
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        raise Redirect('publicauth-extra', self.provider)

    def get_extra_data(self, response):
        user_id = urlparse.parse_qs(response, keep_blank_values=False)['user_id'][0]
        url = self.API_URL % user_id
        response, content = httplib2.Http().request(url)
        result = dict()
        if response[ 'status' ] == 200:
            result = simplejson.loads(content)
        return result

    def extract_data(self, extra, backend_field, form_field):
        return {form_field: extra.get(backend_field, '')}

    def __get_url( self, token=None, http_url=None, parameters=dict() ):
        request = Request.from_consumer_and_token( self.consumer,
                    token = token,
                    http_url=http_url,
                    parameters=parameters)
        request.sign_request(self.signature_method, self.consumer, token)
        return request.to_url()

