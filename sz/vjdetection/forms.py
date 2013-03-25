from django import forms
from sz.vjdetection.detectors import CascadeFileManager


class UploadPhotoForm(forms.Form):
    photo = forms.ImageField()
    haar_cascade = forms.ChoiceField(choices=CascadeFileManager.choices())
    #scaleFactor = forms.FloatField
