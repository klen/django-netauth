" Settings for tests. "
from settings.project import *

# Databases
DATABASES=  {
        'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                    'USER': '',
                    'PASSWORD': '',
                    'TEST_CHARSET': 'utf8',
                }
            }
