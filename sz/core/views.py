from django.http import HttpResponse
from django.shortcuts import redirect

from .models import RegistrationProfile


def index(request):
    return redirect('/client/app/index.html')

def activate(request, activation_key):
    if RegistrationProfile.objects.activate(activation_key):
        return redirect('sz.core.views.index')
    else:
        return HttpResponse("Yosick is upset. "
                            "Bad activation key :'(")
