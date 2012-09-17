# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from sz.clothes.models import Tag
from sz.clothes import services



def tags(request):
    message = request.POST['message']
    tags = Tag.objects.all().order_by('-name')
    tags = services.spellcorrector_tagging_service(message, tags)
    return HttpResponse(simplejson.dumps({"tags": tags}, ensure_ascii=False), mimetype="application/json")