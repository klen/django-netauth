import logging


__version__ = VERSION = '0.1.1'
__project__ = PROJECT = 'django-netauth'


LOG = logging.getLogger( __name__ )


class RedirectException(Exception):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        super( RedirectException, self ).__init__( *args, **kwargs )
