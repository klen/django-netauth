import logging


VERSION_INFO = (0, 1, 6)

__version__ = VERSION = '.'.join(map(str, VERSION_INFO ))
__project__ = PROJECT = 'django-netauth'
__author__ = AUTHOR = "Kirill Klenov <horneds@gmail.com>"
__license__ = LICENSE = "GNU LGPL"


NETAUTH_LOG = logging.getLogger( __name__ )


class RedirectException(Exception):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        super( RedirectException, self ).__init__( *args, **kwargs )
