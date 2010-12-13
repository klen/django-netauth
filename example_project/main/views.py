from StringIO import StringIO

from django.core.serializers.json import Serializer
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.views.generic import TemplateView


class TemplateContextView( TemplateView ):
    """ Allow define context in as_view method.
    """
    context = dict()

    def get(self, request, *args, **kwargs):
        self.context.update(self.get_context_data(**kwargs))
        return self.render_to_response(self.context)


class AbstractEncoderMixin( object ):
    """ Abstract class for data serialize.
    """
    mimetype = "application/text"

    def encode( self, context ):
        raise NotImplementedError()

    def render_to_response(self, context):
        response = self.encode(context)
        return HttpResponse(response, mimetype= self.mimetype)


class JSONViewMixin( AbstractEncoderMixin ):
    """ Serialize queryset or any objects context in JSON.
    """
    mimetype = "application/json"

    def encode( self, context ):
        encoder = Serializer()
        if isinstance(context, QuerySet):
            return encoder.serialize(context, ensure_ascii=False)
        else:
            encoder.objects = context
            encoder.options = dict()
            encoder.stream = StringIO()
            encoder.end_serialization()
            return encoder.getvalue()


class JSONView( JSONViewMixin, TemplateContextView):
    """ Render view context in JSON.
    """
    def get_context_data( self, **kwargs ):
        raise NotImplementedError()
