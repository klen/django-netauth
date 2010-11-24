from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.contrib import messages, auth

from public.exceptions import Redirect
from publicauth import settings, lang
from publicauth.models import PublicID
from publicauth.utils import str_to_class


class PublicBackend(object):
    """ Add this Authentication Backend to
        AUTHENTICATION_BACKENDS tuple in your settings.py
    """

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, identity=None, provider=None):
        """ Authenticate user by public identity.
        """
        if identity:
            try:
                user = PublicID.objects.get(identity=identity, provider=provider).user
                return user
            except PublicID.DoesNotExist:
                return None
        else:
            return None


class BaseBackend(object):

    PROFILE_MAPPING = property(lambda self: getattr(global_settings, "%s_PROFILE_MAPPING" % self.provider.upper(), {}))

    def __init__(self, provider):
        self.provider = provider
        self.identity = None

    def begin(self, request, data):
        raise NotImplementedError

    def complete(self, request, response):
        raise NotImplementedError

    def validate(self, request, data):
        raise NotImplementedError

    def get_extra_data(self, response):
        raise NotImplementedError

    def merge_accounts(self, request):
        """
        Attach PublicID account to regular django
        account and then redirect user. In this situation
        user dont have to fill extra fields because he filled
        them when first account (request.user) was created.

        Note that self.indentity must be already set in this stage by
        validate_response function.
        """
        # create new public ID record in database
        # and attach it to request.user account.
        publicid = PublicID()
        publicid.user = request.user
        publicid.identity = self.identity
        publicid.provider = self.provider
        publicid.save()

        # show nice message to user.
        messages.add_message(request, messages.SUCCESS, lang.ACCOUNTS_MERGED)
        # redirect user.
        raise Redirect(global_settings.LOGIN_REDIRECT_URL)

    def login_user(self, request):
        """
        Try to login user by public identity.
        Do nothing in case of failure.
        """
        # only actavted users can login if activation required.
        user = auth.authenticate(identity=self.identity, provider=self.provider)
        if user and settings.PUBLICAUTH_ACTIVATION_REQUIRED and not user.is_active:
            messages.add_message(request, messages.ERROR, lang.NOT_ACTIVATED)
            raise Redirect(settings.ACTIVATION_REDIRECT_URL)

        # authenticate and redirect user.
        if user:
            messages.add_message(request, messages.SUCCESS, lang.SUCCESSFULLY_AUTHENTICATED)
            auth.login(request, user)

            try:
                redirect_url = request.session['next_url']
                del request.session['next_url']
            except KeyError:
                redirect_url = global_settings.LOGIN_REDIRECT_URL
            raise Redirect(redirect_url)

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


