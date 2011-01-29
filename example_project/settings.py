import os.path

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# NETAUTH_SETTINGS
AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.ModelBackend', 'netauth.auth.NetBackend', )

YANDEX_APPLICATION_ID = "51a38f59a8cf4e96b7635d33a5b37bfe"

FACEBOOK_APPLICATION_ID = "124962940900708"
FACEBOOK_APPLICATION_SECRET = "626e88ccb61ff09ed2416b9f0b93cf08"

TWITTER_CONSUMER_KEY = "vD7tukEla4lJzBPr4BU4hw"
TWITTER_CONSUMER_SECRET = "Uf5KDzDQ8pugSx7502i1GMlj19SAmdw64jFc7nKA"

VKONTAKTE_APPLICATION_ID = "2045136"
VKONTAKTE_APPLICATION_SECRET = "Fj9ROpKBcYSE2MkEr5zo"

# Debug
DEBUG = True
TEMPLATE_DEBUG = True

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'USER': '', 'PASSWORD': '',
        'TEST_CHARSET': 'utf8',
    }}

# Base urls config
ROOT_URLCONF = 'main.urls'

# Media settigns
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = MEDIA_ROOT + 'admin/'

# Templates settings
TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_ROOT, followlinks=True):
    if 'templates' in dirs:
        TEMPLATE_DIRS += (os.path.join(root, 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'main',
    'netauth',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Base apps settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Localization
USE_I18N = True
MIDDLEWARE_CLASSES += ('django.middleware.locale.LocaleMiddleware',)
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

# Debug
INTERNAL_IPS = ('127.0.0.1',)
