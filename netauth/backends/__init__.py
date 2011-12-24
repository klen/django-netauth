import urlparse

from django.contrib import messages, auth
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from httplib2 import Http
from oauth2 import Request

from netauth import NETAUTH_LOG, settings, lang
from netauth.models import NetID
from netauth.utils import str_to_class


class BaseBackend(object):

    PROFILE_MAPPING = property(lambda self: getattr(settings, "%s_PROFILE_MAPPING" % self.provider.upper(), {}))

    def __init__(self, provider):
        self.provider = provider
        self.identity = None

    def begin(self, request, data):
        raise NotImplementedError

    def validate(self, request, data):
        raise NotImplementedError

    def get_extra_data(self, response):
        raise NotImplementedError

    def extract_data(self, extra, backend_field):
        return extra.get(backend_field, '')

    def complete(self, request, response):
        """ Complete net auth.
        """
        extra = self.get_extra_data(response)
        data = {}
        for form_field, backend_field in self.PROFILE_MAPPING.items():
            data[form_field] = self.extract_data(extra, backend_field)
        request.session['extra'] = data

        if settings.ACCEPT_EXTRA_FORM:
            self.fill_extra_fields(request, data)

        request.session['identity'] = self.identity
        return redirect('netauth-extra', self.provider)

    def merge_accounts(self, request):
        """
        Attach NetID account to regular django
        account and then redirect user. In this situation
        user dont have to fill extra fields because he filled
        them when first account (request.user) was created.

        Note that self.indentity must be already set in this stage by
        validate_response function.
        """
        # create new net ID record in database
        # and attach it to request.user account.
        try:
            netid = NetID.objects.get(identity=self.identity, provider=self.provider)
        except NetID.DoesNotExist:
            netid = NetID(user=request.user, identity=self.identity, provider=self.provider)
            netid.save()
            # show nice message to user.
            messages.add_message(request, messages.SUCCESS, lang.ACCOUNTS_MERGED)

    def login_user(self, request):
        """
        Try to login user by net identity.
        Do nothing in case of failure.
        """
        # only actavted users can login if activation required.
        user = auth.authenticate(identity=self.identity, provider=self.provider)
        if user and settings.ACTIVATION_REQUIRED and not user.is_active:
            messages.add_message(request, messages.ERROR, lang.NOT_ACTIVATED)
            return redirect(settings.ACTIVATION_REDIRECT_URL)
        # login
        if user:
            auth.login(request, user)
            return True

        return False

    def fill_extra_fields(self, request, data):
        """
        Try to fetch extra data from provider, if this data is enough
        to validate settings.EXTRA_FORM then call save method of form
        class and login the user.

        The extra parameter can be some complex object
        this is why we use method function 'extra_data' to
        extract data from this object.

        Also we need to create a dictionary with remapped
        keys from profile mapping settings.
        """
        form = str_to_class(settings.EXTRA_FORM)(data)
        if form.is_valid():
            form.save(request, self.identity, self.provider)
            self.login_user(request)
        else:
            return data

    def error(self, request):
        messages.error(request, getattr( lang, '%s_INVALID_RESPONSE' % self.provider.upper()))
        return redirect('netauth-login')


class OAuthBaseBackend(BaseBackend):

    REQUEST_TOKEN_URL = property(lambda self: getattr(settings, "%s_REQUEST_TOKEN_URL" % self.provider.upper()))
    AUTHORIZE_URL = property(lambda self: getattr(settings, "%s_AUTHORIZE_URL" % self.provider.upper()))
    ACCESS_TOKEN_URL = property(lambda self: getattr(settings, "%s_ACCESS_TOKEN_URL" % self.provider.upper()))
    API_URL = property(lambda self: getattr(settings, "%s_API_URL" % self.provider.upper()))

    def __init__( self, *args, **kwargs ):
        self.client = Http()
        super( OAuthBaseBackend, self ).__init__( *args, **kwargs )

    def get_callback( self, request ):
        return request.build_absolute_uri(reverse('netauth-complete', args=[self.provider]))

    def load_request( self, request ):
        response, content = self.client.request(request.to_url())
        NETAUTH_LOG.info(content)

        if response[ 'status' ] != '200':
            NETAUTH_LOG.info(request.to_url())
            return None

        return content

    def get_request(self, url=None, parameters=None):
        return Request(url=url, parameters=parameters)

    @staticmethod
    def parse_qs( content ):
        return urlparse.parse_qs( content, keep_blank_values=False )
