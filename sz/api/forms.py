# -*- coding: utf-8 -*-
from django import forms
from sz.core import models


class FeedRequestForm(forms.Form):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    #accuracy = forms.FloatField(required=False, initial=20, label=u'Погрешность')
    query = forms.CharField(required=False, label=u'Запрос')
    nearby = forms.IntegerField(required=False, min_value=0, max_value=5000, label=u'Удалённость', initial=0)
    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(), required = False, label=u'Категория', to_field_name='alias')


class NearestCityRequestForm(forms.Form):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
