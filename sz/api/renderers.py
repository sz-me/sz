import string
from django import forms
from django.http.multipartparser import parse_header
from django.template import RequestContext, loader
from django.utils import simplejson as json
from rest_framework import serializers, parsers, VERSION
from rest_framework.renderers import BaseRenderer
from rest_framework.request import clone_request
from rest_framework.settings import api_settings
from rest_framework.utils import encoders
from rest_framework.utils.breadcrumbs import get_breadcrumbs

class UnicodeJSONRenderer(BaseRenderer):
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

class BrowsableAPIRenderer(BaseRenderer):
    """
    HTML renderer used to self-document the API.
    """
    media_type = 'text/html'
    format = 'api'
    template = 'rest_framework/api.html'

    def get_default_renderer(self, view):
        """
        Return an instance of the first valid renderer.
        (Don't use another documenting renderer.)
        """
        renderers = [renderer for renderer in view.renderer_classes
                     if not issubclass(renderer, BrowsableAPIRenderer)]
        if not renderers:
            return None
        return renderers[0]()

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

    def get_form(self, view, method, request):
        """
        Get a form, possibly bound to either the input or output data.
        In the absence on of the Resource having an associated form then
        provide a form that can be used to submit arbitrary content.
        """
        if not method in view.allowed_methods:
            return  # Not a valid method

        if not api_settings.FORM_METHOD_OVERRIDE:
            return  # Cannot use form overloading

        request = clone_request(request, method)
        if not view.has_permission(request):
            return  # Don't have permission

        if method == 'DELETE' or method == 'OPTIONS':
            return True  # Don't actually need to return a form

        if (not getattr(view, 'get_serializer', None) or
            not parsers.FormParser in getattr(view, 'parser_classes')):
            media_types = [parser.media_type for parser in view.parser_classes]
            return self.get_generic_content_form(media_types)

        #####
        # TODO: This is a little bit of a hack.  Actually we'd like to remove
        #       this and just render serializer fields to html directly.

        #  We need to map our Fields to Django's Fields.
        field_mapping = {
            serializers.FloatField: forms.FloatField,
            serializers.IntegerField: forms.IntegerField,
            serializers.DateTimeField: forms.DateTimeField,
            serializers.DateField: forms.DateField,
            serializers.EmailField: forms.EmailField,
            serializers.CharField: forms.CharField,
            serializers.BooleanField: forms.BooleanField,
            serializers.PrimaryKeyRelatedField: forms.ModelChoiceField,
            serializers.ManyPrimaryKeyRelatedField: forms.ModelMultipleChoiceField
        }

        # Creating an on the fly form see: http://stackoverflow.com/questions/3915024/dynamically-creating-classes-python
        fields = {}
        obj, data = None, None
        if getattr(view, 'object', None):
            obj = view.object

        serializer = view.get_serializer(instance=obj)
        for k, v in serializer.get_fields(True).items():
            if getattr(v, 'readonly', True):
                continue

            kwargs = {}
            if getattr(v, 'queryset', None):
                kwargs['queryset'] = getattr(v, 'queryset', None)

            try:
                fields[k] = field_mapping[v.__class__](**kwargs)
            except KeyError:
                fields[k] = forms.CharField()

        OnTheFlyForm = type("OnTheFlyForm", (forms.Form,), fields)
        if obj and not view.request.method == 'DELETE':  # Don't fill in the form when the object is deleted
            data = serializer.data
        form_instance = OnTheFlyForm(data)
        return form_instance

    def get_generic_content_form(self, media_types):
        """
        Returns a form that allows for arbitrary content types to be tunneled
        via standard HTML forms.
        (Which are typically application/x-www-form-urlencoded)
        """

        # If we're not using content overloading there's no point in supplying a generic form,
        # as the view won't treat the form's value as the content of the request.
        if not (api_settings.FORM_CONTENT_OVERRIDE
                and api_settings.FORM_CONTENTTYPE_OVERRIDE):
            return None

        content_type_field = api_settings.FORM_CONTENTTYPE_OVERRIDE
        content_field = api_settings.FORM_CONTENT_OVERRIDE
        choices = [(media_type, media_type) for media_type in media_types]
        initial = media_types[0]

        # NB. http://jacobian.org/writing/dynamic-form-generation/
        class GenericContentForm(forms.Form):
            def __init__(self):
                super(GenericContentForm, self).__init__()

                self.fields[content_type_field] = forms.ChoiceField(
                    label='Content Type',
                    choices=choices,
                    initial=initial
                )
                self.fields[content_field] = forms.CharField(
                    label='Content',
                    widget=forms.Textarea
                )

        return GenericContentForm()

    def get_name(self, view):
        try:
            return view.get_name()
        except AttributeError:
            return view.__doc__

    def get_description(self, view):
        try:
            return view.get_description(html=True)
        except AttributeError:
            return view.__doc__

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders *obj* using the :attr:`template` set on the class.

        The context used in the template contains all the information
        needed to self-document the response to this request.
        """
        accepted_media_type = accepted_media_type or ''
        renderer_context = renderer_context or {}

        view = renderer_context['view']
        request = renderer_context['request']
        response = renderer_context['response']

        renderer = self.get_default_renderer(view)
        content = self.get_content(renderer, data, accepted_media_type, renderer_context)

        put_form = self.get_form(view, 'PUT', request)
        post_form = self.get_form(view, 'POST', request)
        delete_form = self.get_form(view, 'DELETE', request)
        options_form = self.get_form(view, 'OPTIONS', request)

        name = self.get_name(view)
        description = self.get_description(view)
        breadcrumb_list = get_breadcrumbs(request.path)

        template = loader.get_template(self.template)
        context = RequestContext(request, {
            'content': content,
            'view': view,
            'request': request,
            'response': response,
            'description': description,
            'name': name,
            'version': VERSION,
            'breadcrumblist': breadcrumb_list,
            'allowed_methods': view.allowed_methods,
            'available_formats': [renderer.format for renderer in view.renderer_classes],
            'put_form': put_form,
            'post_form': post_form,
            'delete_form': delete_form,
            'options_form': options_form,
            'api_settings': api_settings
        })

        ret = template.render(context)

        # Munge DELETE Response code to allow us to return content
        # (Do this *after* we've rendered the template so that we include
        # the normal deletion response code in the output)
        if response.status_code == 204:
            response.status_code = 200

        return ret
