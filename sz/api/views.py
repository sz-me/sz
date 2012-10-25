# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from sz.core.models import DomainTag
from sz.api import services
from djangorestframework.renderers import \
    JSONPRenderer, DocumentingHTMLRenderer, DocumentingXHTMLRenderer, \
    DocumentingPlainTextRenderer, XMLRenderer, YAMLRenderer
from djangorestframework.compat import yaml
from djangorestframework.views import View
from sz.api import forms
from sz.api.renderers import JSONRenderer


SZ_API_RENDERERS = (
    JSONRenderer,
    JSONPRenderer,
    DocumentingHTMLRenderer,
    DocumentingXHTMLRenderer,
    DocumentingPlainTextRenderer,
    XMLRenderer
    )

if yaml:
    SZ_API_RENDERERS += (YAMLRenderer, )
else:
    YAMLRenderer = None



class PlaceSearchView(View):
    form = forms.PlaceSearchForm
    renderers = SZ_API_RENDERERS
    def post(self, request):
        print self.renderers
        position = {
            'latitude': self.CONTENT['latitude'],
            'longitude': self.CONTENT['longitude'],
            'accuracy': self.CONTENT['accuracy'],
        }
        if self.CONTENT['query']:
            query = u"%s" % self.CONTENT['query']
        else:
            query = None
        response = services.venue_location_search_service(position, query)
        return response

def tags(request):
    message = request.POST.get('message')
    tags = DomainTag.objects.all().order_by('-name')
    tags = services.spellcorrector_tagging_service(message, tags)
    return HttpResponse(simplejson.dumps({"tags": tags}, ensure_ascii=False), mimetype="application/json")