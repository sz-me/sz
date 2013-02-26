# -*- coding: utf-8 -*-
from rest_framework import status
from sz.api import forms, serializers, response as sz_api_response
from sz.api.views import SzApiView, FilteredListView, categorization_service


class CategoriesRoot(SzApiView):
    """ List of available categories of clothes """

    def get(self, request, format=None):
        categories = categorization_service.get_categories()
        serializer = serializers.CategorySerializer(instance=categories)
        return sz_api_response.Response(serializer.data)


class CategoriesDetect(FilteredListView):
    """ Detect categories of clothes in a text """

    request_form_class = forms.CategoriesDetectingRequestForm

    def get(self, request, format=None):
        params = self.get_request_params(request)
        categories = categorization_service.detect_categories(params['text'])
        serializer = serializers.CategorySerializer(instance=categories)
        return sz_api_response.Response(serializer.data)


class CategoriesInstance(SzApiView):
    """ Retrieve a category of clothes """

    def get(self, request, pk, format=None):
        categories = categorization_service.get_categories()
        filtered_categories = filter(lambda c: ("%s" % c.pk) == pk, categories)
        if len(filtered_categories) == 0:
            filtered_categories = filter(lambda c: c.alias == pk, categories)
        if len(filtered_categories) == 0:
            return sz_api_response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CategorySerializer(instance=filtered_categories[0])
        return sz_api_response.Response(serializer.data)
