from django.conf import settings as django_settings
from django.template import Library

from netauth import settings as netauth_settings


register = Library()

def option( value, name ):
    """ Return settings parameter from django or netauth settings.
    """
    return getattr(django_settings, name) or getattr(netauth_settings, name) or ''

register.filter(option)


def vk_widget():
    """ Render vkontakte widget.
    """
    return dict( VKONTAKTE_APPLICATION_ID = django_settings.VKONTAKTE_APPLICATION_ID )

register.inclusion_tag('netauth/vk_widget.html')(vk_widget)
