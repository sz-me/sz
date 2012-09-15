# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from sz.clothes.models import Pattern
from sz.clothes import services



def tags(request):
    message = request.POST['message']
    patterns = Pattern.objects.all().order_by('-value')
    tags = services.tags(message, patterns)
    return HttpResponse(simplejson.dumps({"tags": tags}, ensure_ascii=False), mimetype="application/json")