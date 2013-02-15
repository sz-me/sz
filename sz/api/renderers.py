# -*- coding: utf-8 -*-
from django.http.multipartparser import parse_header
#from django.utils import simplejson as json
import json
from rest_framework import renderers as rest_framework_renderers
from rest_framework.utils import encoders

class UnicodeJSONRenderer(rest_framework_renderers.BaseRenderer):
    """
    Renderer which serializes to json.
    """

    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `obj` into json.
        """
        if data is None:
            return ''

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowseableAPIRenderer.
        renderer_context = renderer_context or {}
        indent = renderer_context.get('indent', None)

        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            base_media_type, params = parse_header(accepted_media_type)
            indent = params.get('indent', indent)
            try:
                indent = max(min(int(indent), 8), 0)
            except (ValueError, TypeError):
                indent = None

        return json.dumps(data, cls=self.encoder_class, indent=indent, ensure_ascii=False)

class BrowsableAPIRenderer(rest_framework_renderers.BrowsableAPIRenderer):
    """
    HTML renderer used to self-document the API.
    """
    def get_content(self, renderer, data,
                    accepted_media_type, renderer_context):
        """
        Get the content as if it had been rendered by the default
        non-documenting renderer.
        """
        if not renderer:
            return '[No renderers were found]'

        renderer_context['indent'] = 4
        content = renderer.render(data, accepted_media_type, renderer_context)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #if not all(char in string.printable for char in content):
        #    return '[%d bytes of binary content]'

        return content
