from __future__ import absolute_import

import urllib
import urlparse

from oauth.oauth import OAuthConsumer, OAuthToken, OAuthRequest, OAuthSignatureMethod_HMAC_SHA1

from django.conf import settings as global_settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib import messages

from public.exceptions import Redirect
from publicauth.backends import BaseBackend
from publicauth import lang


class OAuthBackend(BaseBackend):

    CONSUMER_KEY = property(lambda self: getattr(global_settings, "%s_CONSUMER_KEY" % self.provider.upper()))
    CONSUMER_SECRET = property(lambda self: getattr(global_settings, "%s_CONSUMER_SECRET" % self.provider.upper()))
    REQUEST_TOKEN_URL = property(lambda self: getattr(global_settings, "%s_REQUEST_TOKEN_URL" % self.provider.upper()))
    ACCESS_TOKEN_URL = property(lambda self: getattr(global_settings, "%s_ACCESS_TOKEN_URL" % self.provider.upper()))
    AUTHORIZE_URL = property(lambda self: getattr(global_settings, "%s_AUTHORIZE_URL" % self.provider.upper()))
    API_URL = property(lambda self: getattr(global_settings, "%s_API_URL" % self.provider.upper()))

    def begin(self, request, data):
        """
        Try to get Request Token from OAuth Provider and
        redirect user to provider's site for approval.
        """
        consumer = OAuthConsumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        signature_method = OAuthSignatureMethod_HMAC_SHA1()
        callback = request.build_absolute_uri(reverse('publicauth-complete', args=[self.provider]))
        oauth_req = OAuthRequest.from_consumer_and_token(consumer, callback=callback, http_url=self.REQUEST_TOKEN_URL)
        oauth_req.sign_request(signature_method, consumer, None)
        response = urllib.urlopen(oauth_req.to_url()).read()

        token = OAuthToken.from_string(response) # instatiate token

        oauth_req = OAuthRequest.from_consumer_and_token(consumer, token, http_url=self.AUTHORIZE_URL)
        oauth_req.sign_request(signature_method, consumer, token)
        raise Redirect(oauth_req.to_url())

    def validate(self, request, data):
        signature_method = OAuthSignatureMethod_HMAC_SHA1()
        consumer = OAuthConsumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        try:
            oauth_token = data['oauth_token']
            oauth_verifier = data.get('oauth_verifier', None)
        except MultiValueDictKeyError:
            messages.error(request, lang.BACKEND_ERROR)
            raise Redirect('publicauth-login')
        oauth_req = OAuthRequest.from_consumer_and_token(consumer, http_url=self.ACCESS_TOKEN_URL)
        oauth_req.set_parameter('oauth_token', oauth_token)
        if oauth_verifier:
            oauth_req.set_parameter('oauth_verifier', oauth_verifier)
        oauth_req.sign_request(signature_method, consumer, None)
        response = urllib.urlopen(oauth_req.to_url()).read()
        self.identity = urlparse.parse_qs(response, keep_blank_values=False)['oauth_token'][0]
        return response

    def complete(self, request, response):
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        raise Redirect('publicauth-extra', self.provider)

    def get_extra_data(self, response):
        user_id = urlparse.parse_qs(response, keep_blank_values=False)['user_id'][0]
        url = self.API_URL % user_id
        return simplejson.loads(urllib.urlopen(url).read())

    def extract_data(self, extra, backend_field, form_field):
        return {form_field: extra.get(backend_field, '')}

