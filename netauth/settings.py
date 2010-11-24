from django.conf import settings


# To disable registration, set it to False
REGISTRATION_ALLOWED = getattr(settings, "NETAUTH_REGISTRATION_ALLOWED", True)

# This dict contains mapping of SREG fields to AX uris, you probably don't need to change it
# http://www.axschema.org/types/
AX_URIS = getattr(settings, "NETAUTH_AX_URIS", {
    'nickname': 'http://axschema.org/namePerson/friendly',
    'email': 'http://axschema.org/contact/email',
    'fullname': 'http://axschema.org/namePerson',
    'dob': 'http://axschema.org/birthDate',
    'gender': 'http://axschema.org/person/gender',
    'postcode': 'http://axschema.org/contact/postalCode/home',
    'country': 'http://axschema.org/contact/country/home',
    'language': 'http://axschema.org/pref/language',
    'timezone': 'http://axschema.org/pref/timezone',
})

BACKEND_MAPPING = getattr(settings, "NETAUTH_BACKEND_MAPPING", {
    'openid': 'netauth.backends.openid.OpenIDBackend',
    'google': 'netauth.backends.google.GoogleBackend',
    'twitter': 'netauth.backends.oauth.OAuthBackend',
    'facebook': 'netauth.backends.facebook.FacebookBackend',
    'friendfeed': 'netauth.backends.oauth.OAuthBackend',
    'vkontakte': 'netauth.backends.vkontakte.VkontakteBackend',
    }
)

REGISTRATION_DISABLED_REDIRECT = getattr(settings, "NETAUTH_REGISTRATION_DISABLED_REDIRECT", "/")

ACTIVATION_REQUIRED = getattr(settings, "NETAUTH_ACTIVATION_REQUIRED", False)

ACTIVATION_REDIRECT_URL = getattr(settings, "NETAUTH_ACTIVATION_REDIRECT_URL", "/")

EXTRA_FORM = getattr(settings, "NETAUTH_EXTRA_FORM", "netauth.forms.ExtraForm")

# Django settings
DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL")
LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL")
LOGOUT_URL = getattr(settings, "LOGOUT_URL")

# OAuth providers settings
TWITTER_ACCESS_TOKEN_URL = getattr(settings, "TWITTER_ACCESS_TOKEN_URL", "https://api.twitter.com/oauth/access_token")
TWITTER_AUTHORIZE_URL = getattr(settings, "TWITTER_AUTHORIZE_URL", "https://api.twitter.com/oauth/authorize")
TWITTER_API_URL = getattr(settings, "TWITTER_API_URL", "http://api.twitter.com/1/users/show.json?user_id=%s")
TWITTER_PROFILE_MAPPING = getattr(settings, "TWITTER_PROFILE_MAPPING", {
    'screen_name': 'username',
})

FACEBOOK_AUTHORIZE_URL = getattr(settings, "FACEBOOK_AUTHORIZE_URL", "https://graph.facebook.com/oauth/authorize")
FACEBOOK_ACCESS_TOKEN_URL = getattr(settings, "FACEBOOK_ACCESS_TOKEN_URL", "https://graph.facebook.com/oauth/access_token")
FACEBOOK_API_URL = getattr(settings, "FACEBOOK_API_URL", "https://graph.facebook.com/me")
