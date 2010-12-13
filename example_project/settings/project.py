from settings.core import *

# PROJECT SETTINGS
# -----------------
INSTALLED_APPS += (

    # Community apps
    'south',

    # Base project app
    'main',

)
CACHE_PREFIX = "PROD"


# NETAUTH
# --------
INSTALLED_APPS += ( 'netauth',)
MIDDLEWARE_CLASSES += ( 'netauth.middleware.RedirectMiddleware', )
AUTHENTICATION_BACKENDS = ( 'netauth.auth.NetBackend', )

YANDEX_APPLICATION_ID = "51a38f59a8cf4e96b7635d33a5b37bfe"

FACEBOOK_APPLICATION_ID = "124962940900708"
FACEBOOK_APPLICATION_SECRET = "626e88ccb61ff09ed2416b9f0b93cf08"

TWITTER_CONSUMER_KEY = "vD7tukEla4lJzBPr4BU4hw"
TWITTER_CONSUMER_SECRET = "Uf5KDzDQ8pugSx7502i1GMlj19SAmdw64jFc7nKA"

VKONTAKTE_APPLICATION_ID = "2045136"
VKONTAKTE_APPLICATION_SECRET = "Fj9ROpKBcYSE2MkEr5zo"
