from django.conf import settings as django_settings
from django.template import Library

from netauth import settings as netauth_settings


register = Library()

def option( value, name ):
    """ Return settings parameter from django or netauth settings.
    """
    return getattr(django_settings, name, '') or getattr(netauth_settings, name, '')

register.filter(option)
