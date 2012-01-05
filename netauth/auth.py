from django.contrib.auth.models import User

from netauth.models import NetID


class NetBackend(object):
    """
    Add this Authentication Backend to
    AUTHENTICATION_BACKENDS tuple in your settings.py
    """
    supports_object_permissions = False
    supports_anonymous_user = True

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(identity=None, provider=None):
        " Authenticate user by net identity. "
        if not identity:
            return None

        try:
            netid = NetID.objects.get(identity=identity, provider=provider)
            return netid.user
        except NetID.DoesNotExist:
            return None
