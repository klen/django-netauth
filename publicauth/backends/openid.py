from __future__ import absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from openid.consumer import consumer, discover
from openid.extensions.ax import FetchRequest, AttrInfo
from openid.extensions.sreg import SRegRequest, SRegResponse

from publicauth.exceptions import Redirect
from publicauth import settings, lang
from publicauth.backends import BaseBackend


class OpenIDBackend(BaseBackend):

    def begin(self, request, data):
        try:
            openid_url = data['openid_url'].strip()
        except KeyError:
            messages.error(request, lang.FILL_OPENID_URL)
            raise Redirect('publicauth-login')

        # allow user to type openid provider without http:// prefix
        if not openid_url.startswith("http"):
            openid_url = "http://%s" % openid_url

        return_url = request.build_absolute_uri(reverse('publicauth-complete', args=[self.provider]))
        request.session['openid_return_to'] = return_url
        client = consumer.Consumer(request.session, None)

        try:
            openid_request = client.begin(openid_url)
            sreg_extra = [i for i in self.PROFILE_MAPPING]
            sreg = SRegRequest(required=sreg_extra)
            openid_request.addExtension(sreg)
            ax_msg = FetchRequest()
            for detail in self.PROFILE_MAPPING:
                ax_msg.add(AttrInfo(settings.AX_URIS[detail], required=True))
            openid_request.addExtension(ax_msg)

            redirect_url = openid_request.redirectURL(realm='http://' + request.get_host(), return_to=return_url)
            raise Redirect(redirect_url)

        except discover.DiscoveryFailure:
            messages.error(request, _('Could not find OpenID server'))
            raise Redirect('publicauth-login')

    def validate(self, request, data):
        """
        Validate response from OpenID server.
        Set identity in case of successfull validation.
        """
        client = consumer.Consumer(request.session, None)

        try:
            resp = client.complete(data, request.session['openid_return_to'])
        except KeyError:
            messages.error(request, lang.INVALID_RESPONSE_FROM_OPENID)
            raise Redirect('publicauth-login')
        if resp.status == consumer.CANCEL:
            messages.warning(request, lang.OPENID_CANCELED)
            raise Redirect('publicauth-login')
        elif resp.status == consumer.FAILURE:
            messages.error(request, lang.OPENID_FAILED % resp.message)
            raise Redirect('publicauth-login')
        elif resp.status == consumer.SUCCESS:
            self.identity = resp.identity_url
            del request.session['openid_return_to']
            return resp

    def complete(self, request, response):
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        return redirect('publicauth-extra', self.provider)

    def get_extra_data(self, response):
        return SRegResponse.fromSuccessResponse(response)

