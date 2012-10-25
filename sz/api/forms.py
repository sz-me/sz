# -*- coding: utf-8 -*-
from django import forms

class PlaceSearchForm(forms.Form):
    latitude = forms.FloatField(required = True, min_value = -90.0, max_value = 90.0, label=u'Широта')
    longitude = forms.FloatField(required = True, min_value = -180.0, max_value = 180.0, label=u'Долгота')
    accuracy = forms.FloatField(required = False, initial = 20, label=u'Погрешность')
    query = forms.CharField(required = False, label=u'Название')