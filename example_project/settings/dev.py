from settings.project import *

# Cache
CACHE_PREFIX = "DEV"

# Debug
DEBUG = True
TEMPLATE_DEBUG = True

if DEBUG:
    INTERNAL_IPS += tuple('192.168.1.%s' % x for x in range( 99, 111 ))
    MIDDLEWARE_CLASSES += ( 'debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ( 'debug_toolbar', )
