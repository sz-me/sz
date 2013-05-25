from django.http import HttpResponse
from django.shortcuts import redirect

from .models import RegistrationProfile


def index(request):
    return redirect('/client/app/index.html')

def confirm(request, confirmation_key):
    if RegistrationProfile.objects.confirm_email(
        confirmation_key
    ):
        return redirect('sz.core.views.index')
    else:
        return HttpResponse("Yosick is upset. "
        					"Bad confirmation key :'(")
