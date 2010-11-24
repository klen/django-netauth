from django.utils.translation import ugettext as _
from django.conf import settings


ACTIVATION_REQUIRED_TEXT = getattr(settings, "PUBLICAUTH_ACTIVATION_REQUIRED_TEXT", _('To complete registration, check your email and activate your account'))
REGISTRATION_DISABLED = getattr(settings, "PUBLICAUTH_REGISTRATION_DISABLED", _('We are sorry, but registration is disabled. Come back later'))
FILL_OPENID_URL = getattr(settings, "PUBLICAUTH_FILL_OPENID_URL", _('Please fill openid url field'))
BACKEND_ERROR = getattr(settings, "PUBLICAUTH_BACKEND_ERROR", _('Your authentication provider returned bad response, please try again'))
OPENID_CANCELED = getattr(settings, "PUBLICAUTH_OPENID_CANCELED", _('You have cancelled OpenID authentication'))
OPENID_FAILED = getattr(settings, "PUBLICAUTH_OPENID_FAILED", _('OpenID authentication failed. Reason: %s'))
SUCCESS_LOGOUT = getattr(settings, "PUBLICAUTH_SUCCESS_LOGOUT", _('You have successfully logged out'))
ACCOUNTS_MERGED = getattr(settings, "PUBLICAUTH_ACCOUNTS_MERGED", _('Your existing account was merged with new authentication account'))
NOT_ACTIVATED = getattr(settings, "PUBLICAUTH_NOT_ACTIVATED",  _('Your account is not activated. Please activate it first.'))
SUCCESSFULLY_AUTHENTICATED = getattr(settings, "PUBLICAUTH_SUCCESSFULLY_AUTHENTICATED", _('You have successfully authenticated'))
FACEBOOK_INVALID_RESPONSE = getattr(settings, 
                                    "PUBLICAUTH_FACEBOOK_INVALID_RESPONSE", 
                                    _('Invalid response received from facebook server, please start the authentication process again')
                                    )
INVALID_RESPONSE_FROM_OPENID = getattr(settings, 
                                        "PUBLICAUTH_INVALID_RESPONSE_FROM_OPENID",
                                        ('Invalid response received from OpenID server, please start the authentication process again'))
VKONTAKTE_INVALID_RESPONSE = getattr(settings, 
                                    "PUBLICAUTH_VKONTAKTE_INVALID_RESPONSE", 
                                    _('Invalid response received from vkontakte server, please start the authentication process again')
                                    )
