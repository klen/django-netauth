from __future__ import absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from openid.consumer import consumer, discover
from openid.extensions.ax import FetchRequest, AttrInfo
from openid.extensions.sreg import SRegRequest, SRegResponse

from netauth import settings, lang
from netauth.backends import BaseBackend


class OpenIDBackend(BaseBackend):

    def begin(self, request, data):
        try:
            openid_url = data['openid_url'].strip()
        except KeyError:
            messages.error(request, lang.FILL_OPENID_URL)
            return redirect('netauth-login')

        # allow user to type openid provider without http:// prefix
        if not openid_url.startswith("http"):
            openid_url = "http://%s" % openid_url

        return_url = request.build_absolute_uri(reverse('netauth-complete', args=[self.provider]))
        request.session['openid_return_to'] = return_url
        client = consumer.Consumer(request.session, None)

        try:
            openid_request = client.begin(openid_url)
            sreg_extra = [value for key, value in self.PROFILE_MAPPING.items()]
            sreg = SRegRequest(required=sreg_extra)
            openid_request.addExtension(sreg)
            ax_msg = FetchRequest()
            for key, detail in self.PROFILE_MAPPING.items():
                ax_msg.add(AttrInfo(settings.AX_URIS[detail], required=True))
            openid_request.addExtension(ax_msg)

            redirect_url = openid_request.redirectURL(realm='http://' + request.get_host(), return_to=return_url)
            return redirect(redirect_url)

        except discover.DiscoveryFailure:
            messages.error(request, _('Could not find OpenID server'))
            return redirect('netauth-login')

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
            return redirect('netauth-login')
        if resp.status == consumer.CANCEL:
            messages.warning(request, lang.OPENID_CANCELED)
            return redirect('netauth-login')
        elif resp.status == consumer.FAILURE:
            messages.error(request, lang.OPENID_FAILED % resp.message)
            return redirect('netauth-login')
        elif resp.status == consumer.SUCCESS:
            self.identity = resp.identity_url
            del request.session['openid_return_to']
            return resp

    def get_extra_data(self, response):
        return SRegResponse.fromSuccessResponse(response)

