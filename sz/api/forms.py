# -*- coding: utf-8 -*-
from django import forms
from sz import settings
from sz.core import models


class PaginatedRequestForm(forms.Form):
    max_id = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False, min_value=1, max_value=50, initial=settings.DEFAULT_PAGINATE_BY)
    offset = forms.IntegerField(required=False, min_value=0)


class FeedRequestForm(PaginatedRequestForm):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    #accuracy = forms.FloatField(required=False, initial=20, label=u'Погрешность')
    query = forms.CharField(required=False, label=u'Запрос')
    radius = forms.IntegerField(
        required=False, min_value=0, max_value=5000, label=u'Удалённость', initial=settings.DEFAULT_RADIUS)
    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(), required=False, label=u'Категория')


class PlaceSearchRequestForm(forms.Form):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    query = forms.CharField(required=False, label=u'Запрос')
    radius = forms.IntegerField(
        required=False, min_value=0, max_value=5000, label=u'Удалённость', initial=settings.DEFAULT_RADIUS)


class NearestCityRequestForm(forms.Form):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')


class CategoriesDetectingRequestForm(forms.Form):
    text = forms.CharField(required=True, label=u'Текст')