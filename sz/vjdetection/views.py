from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from sz.vjdetection import forms, detect_face, get_haar_cascade_path

def index(request):
    if request.method == 'POST':
        form = forms.UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            params = form.cleaned_data
            photo = detect_face(params['photo'], get_haar_cascade_path(params['haar_cascade']))
            response = HttpResponse(photo, content_type='image/jpeg')
            return response
    else:
        form = forms.UploadPhotoForm()
    return render_to_response('vjdetection/upload.html', {'form': form}, context_instance=RequestContext(request))
