# Create your views here.
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponse
from sz.core.models import Message
from django.template import RequestContext
from django.http import Http404
from django.db.utils import DatabaseError

def index(request):
    try:
        feed = Message.objects.all().order_by('-date')
    except DatabaseError: 
        raise Http404
    return render_to_response(
        'feed/index.html', 
        {'feed': feed}, 
        context_instance = RequestContext(request))

def light(request):
    try:
        pass
    except DatabaseError:
        raise Http404
    return render_to_response(
        'feed/light.html',
        {},
        context_instance = RequestContext(request))