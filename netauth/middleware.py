from django.shortcuts import redirect
from netauth.exceptions import Redirect

class RedirectMiddleware(object):
    """ You must add this middleware to MIDDLEWARE_CLASSES list,
        to make work Redirect exception. All arguments passed to
        Redirect will be passed to django built in redirect function.
    """
    def process_exception(self, request, exception):
        if not isinstance(exception, Redirect):
            return
        return redirect(*exception.args, **exception.kwargs)
