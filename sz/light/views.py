# Create your views here.
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponse
from sz.core.models import Message
from django.template import RequestContext
from django.http import Http404
from django.db.utils import DatabaseError

def index(request):
    return render_to_response(
        'light/index.html',
        {},
        context_instance = RequestContext(request))

def backbone(request):
    return render_to_response(
        'light/backbone.html',
        {},
        context_instance = RequestContext(request))
