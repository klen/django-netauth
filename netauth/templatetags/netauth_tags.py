from django.conf import settings as django_settings
from django.template import Library, Token, TOKEN_BLOCK, Node, Variable

from netauth import settings as netauth_settings


register = Library()

@register.filter
def option( value, name ):
    """ Return settings parameter from django or netauth settings.
    """
    return getattr(django_settings, name, '') or getattr(netauth_settings, name, '')

"""
    This tags from django-misc application - https://github.com/ilblackdragon/django-misc/tree/v0.0.1
    When django-misc app will be in PyPi, it will be removed from here
"""

@register.tag
def set(parser, token):
    """
        Usage:
        {% set templ_tag var1 var2 ... key %}
        {% set variable key %}
        This tag save result of {% templ_tag var1 var2 ... %} to variable with name key,
        Or will save value of variable to new variable with name key.
    """
    bits = token.contents.split(' ')[1:]
    new_token = Token(TOKEN_BLOCK, ' '.join(bits[:-1]))
    if bits[0] in parser.tags:
        func = parser.tags[bits[0]](parser, new_token)
    else:
        func = Variable(bits[0])
    return SetNode(func, bits[-1])

class SetNode(Node):

    def __init__(self, func, key):
        self.func = func
        self.key = key

    def render(self, context):
        if isinstance(self.func, Node):
            context[self.key] = self.func.render(context)
        else:
            context[self.key] = self.func.resolve(context)
        return ''

@register.simple_tag
def get_settings(key, default=None):
    return getattr(settings, key, default)
