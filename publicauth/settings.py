import re

from django import forms
from django.conf import settings


### REGISTRATION_ALLOWED ###########################################################################
# To disable registration, set it to False                                                         #
REGISTRATION_ALLOWED = getattr(settings, "REGISTRATION_ALLOWED", True)                             #
####################################################################################################

### AX_URIS ########################################################################################
# This dict contains mapping of SREG fields to AX uris, you probably don't need to change it       #
# http://www.axschema.org/types/                                                                   #
AX_URIS = getattr(settings, "AX_URIS", {                                                           #
    'nickname': 'http://axschema.org/namePerson/friendly',                                         #
    'email': 'http://axschema.org/contact/email',                                                  #
    'fullname': 'http://axschema.org/namePerson',                                                  #
    'dob': 'http://axschema.org/birthDate',                                                        #
    'gender': 'http://axschema.org/person/gender',                                                 #
    'postcode': 'http://axschema.org/contact/postalCode/home',                                     #
    'country': 'http://axschema.org/contact/country/home',                                         #
    'language': 'http://axschema.org/pref/language',                                               #
    'timezone': 'http://axschema.org/pref/timezone',                                               #
})                                                                                                 #
####################################################################################################

### BACKEND_MAPPING ################################################################################
PUBLICAUTH_BACKEND_MAPPING = getattr(settings, "PUBLICAUTH_BACKEND_MAPPING", {                     #
    'openid': 'publicauth.backends.openid.OpenIDBackend',                                          #
    'google': 'publicauth.backends.google.GoogleBackend',                                          #
    'twitter': 'publicauth.backends.oauth.OAuthBackend',                                           #
    'friendfeed': 'publicauth.backends.oauth.OAuthBackend',                                        #
    'facebook': 'publicauth.backends.facebook.FacebookBackend',                                    #
    'vkontakte': 'publicauth.backends.vkontakte.VkontakteBackend',                                 #
    }                                                                                              #
)                                                                                                  #
####################################################################################################

REGISTRATION_DISABLED_REDIRECT = getattr(settings, "REGISTRATION_DISABLED_REDIRECT", "/")

PUBLICAUTH_ACTIVATION_REQUIRED = getattr(settings, "PUBLICAUTH_ACTIVATION_REQUIRED", False)

ACTIVATION_REDIRECT_URL = getattr(settings, "PUBLICAUTH_ACTIVATION_REDIRECT_URL", "/")

EXTRA_FORM = getattr(settings, "PUBLICAUTH_EXTRA_FORM", "publicauth.forms.ExtraForm")
