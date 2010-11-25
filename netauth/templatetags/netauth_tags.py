from django.conf import settings as django_settings
from django.template import Library

from netauth import settings as netauth_settings


register = Library()

def option( value, name ):
    """ Return settings parameter from django or netauth settings.
    """
    return getattr(django_settings, name) or getattr(netauth_settings, name) or ''

register.filter(option)


def netauth_widget():
    """ Render netauth controls.
    """
    return dict(
            VKONTAKTE_APPLICATION_ID = django_settings.VKONTAKTE_APPLICATION_ID,
            STATIC_URL = django_settings.STATIC_URL )

register.inclusion_tag('netauth/netauth_widget.html')(netauth_widget)
