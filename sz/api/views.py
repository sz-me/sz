# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from sz.core.models import Tag
from sz.api import services

def tags(request):
    message = request.POST['message']
    tags = Tag.objects.all().order_by('-name')
    tags = services.spellcorrector_tagging_service(message, tags)
    return HttpResponse(simplejson.dumps({"tags": tags}, ensure_ascii=False), mimetype="application/json")