class Redirect(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super( Redirect, self ).__init__( *args, **kwargs )
