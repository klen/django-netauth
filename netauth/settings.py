from django.conf import settings


### REGISTRATION_ALLOWED ###########################################################################
# To disable registration, set it to False                                                         #
REGISTRATION_ALLOWED = getattr(settings, "NETAUTH_REGISTRATION_ALLOWED", True)                             #
####################################################################################################

### AX_URIS ########################################################################################
# This dict contains mapping of SREG fields to AX uris, you probably don't need to change it       #
# http://www.axschema.org/types/                                                                   #
AX_URIS = getattr(settings, "NETAUTH_AX_URIS", {                                                           #
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
BACKEND_MAPPING = getattr(settings, "NETAUTH_BACKEND_MAPPING", {                     #
    'openid': 'netauth.backends.openid.OpenIDBackend',                                          #
    'google': 'netauth.backends.google.GoogleBackend',                                          #
    'twitter': 'netauth.backends.oauth.OAuthBackend',                                           #
    'facebook': 'netauth.backends.facebook.FacebookBackend',                                    #
    'friendfeed': 'netauth.backends.oauth.OAuthBackend',                                        #
    'vkontakte': 'netauth.backends.vkontakte.VkontakteBackend',                                 #
    }                                                                                              #
)                                                                                                  #
####################################################################################################

REGISTRATION_DISABLED_REDIRECT = getattr(settings, "NETAUTH_REGISTRATION_DISABLED_REDIRECT", "/")

ACTIVATION_REQUIRED = getattr(settings, "NETAUTH_ACTIVATION_REQUIRED", False)

ACTIVATION_REDIRECT_URL = getattr(settings, "NETAUTH_ACTIVATION_REDIRECT_URL", "/")

EXTRA_FORM = getattr(settings, "NETAUTH_EXTRA_FORM", "netauth.forms.ExtraForm")

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL")

LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")
LOGOUT_URL = getattr(settings, "LOGOUT_URL")
