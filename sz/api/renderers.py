from djangorestframework.renderers import BaseRenderer
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson as json
from djangorestframework.utils.mediatypes import get_media_type_params

class JSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON
    """

    media_type = 'application/json'
    format = 'json'

    def render(self, obj=None, media_type=None):
        """
        Renders *obj* into serialized JSON.
        """
        if obj is None:
            return ''

        # If the media type looks like 'application/json; indent=4', then
        # pretty print the result.
        indent = get_media_type_params(media_type).get('indent', None)
        sort_keys = False
        try:
            indent = max(min(int(indent), 8), 0)
            sort_keys = True
        except (ValueError, TypeError):
            indent = None

        return json.dumps(obj, cls=DateTimeAwareJSONEncoder, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

from djangorestframework.renderers import\
    JSONPRenderer, DocumentingHTMLRenderer, DocumentingXHTMLRenderer,\
    DocumentingPlainTextRenderer, XMLRenderer, YAMLRenderer
from djangorestframework.compat import yaml

SZ_API_DEFAULT_RENDERERS = (
    JSONRenderer,
    JSONPRenderer,
    DocumentingHTMLRenderer,
    DocumentingXHTMLRenderer,
    DocumentingPlainTextRenderer,
    XMLRenderer
    )

if yaml:
    SZ_API_DEFAULT_RENDERERS += (YAMLRenderer, )
else:
    YAMLRenderer = None

