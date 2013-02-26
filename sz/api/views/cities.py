# -*- coding: utf-8 -*-
from rest_framework import permissions, status
from sz.api import forms, response as sz_api_response
from sz.api.views import SzApiView, city_service


class CityNearest(SzApiView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        nearest_city_request = forms.NearestCityRequestForm(request.QUERY_PARAMS)
        if nearest_city_request.is_valid():
            params = nearest_city_request.cleaned_data
            response = city_service.get_city_by_position(params['longitude'], params['latitude'])
            return sz_api_response.Response(response)
        else:
            return sz_api_response.Response(nearest_city_request.errors, status=status.HTTP_400_BAD_REQUEST)
