import logging


VERSION_INFO = (0, 1, 7)

__version__ = VERSION = '.'.join(map(str, VERSION_INFO ))
__project__ = PROJECT = 'django-netauth'
__author__ = AUTHOR = "Kirill Klenov <horneds@gmail.com>"
__license__ = LICENSE = "GNU LGPL"


NETAUTH_LOG = logging.getLogger( __name__ )

