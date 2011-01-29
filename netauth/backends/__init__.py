import urlparse

from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from httplib2 import Http
from oauth2 import Request

from netauth import LOG, RedirectException, settings, lang
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
        return dict()

    def complete(self, request, response):
        """ Complete net auth.
        """
        data = self.fill_extra_fields(request, self.get_extra_data(response))
        request.session['extra'] = data
        request.session['identity'] = self.identity
        raise RedirectException('netauth-extra', self.provider)

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
        netid = NetID()
        netid.user = request.user
        netid.identity = self.identity
        netid.provider = self.provider
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
            raise RedirectException(settings.ACTIVATION_REDIRECT_URL)

        # authenticate and redirect user.
        if user:
            messages.add_message(request, messages.SUCCESS, lang.SUCCESSFULLY_AUTHENTICATED)
            auth.login(request, user)

            try:
                redirect_url = request.session['next_url']
                del request.session['next_url']
            except KeyError:
                redirect_url = settings.LOGIN_REDIRECT_URL
            raise RedirectException(redirect_url)

    def fill_extra_fields(self, request, extra):
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
        data = {}
        if extra:
            for backend_field, form_field in self.PROFILE_MAPPING.items():
                data.update(self.extract_data(extra, backend_field, form_field))

        LOG.info(data)

        form = str_to_class(settings.EXTRA_FORM)(data)
        if form.is_valid():
            form.save(request, self.identity, self.provider)
            self.login_user(request)

        else:
            return data

    def extract_data(self, extra, backend_field, form_field):
        """
        If extra isnt standart python dictionary
        you need to implement this method to retrive
        values from this object.
        """
        return {form_field: extra.get(backend_field, '')}

    def error(self, request):
        messages.error(request, getattr( lang, '%s_INVALID_RESPONSE' % self.provider.upper()))
        raise RedirectException('netauth-login')


class OAuthBaseBackend( BaseBackend ):

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
        LOG.info(content)
        if response[ 'status' ] != '200':
            LOG.info(request.to_url())
            raise RedirectException('netauth-login')

        return content

    def get_request(self, url=None, parameters=None):
        return Request(url=url, parameters=parameters)

    @staticmethod
    def parse_qs( content ):
        return urlparse.parse_qs( content, keep_blank_values=False )
