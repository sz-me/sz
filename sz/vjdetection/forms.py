from django import forms
from sz.vjdetection import get_haar_cascade_choices


class UploadPhotoForm(forms.Form):
    photo = forms.ImageField()
    haar_cascade = forms.ChoiceField(choices=get_haar_cascade_choices())
    #scaleFactor = forms.FloatField
