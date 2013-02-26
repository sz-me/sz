# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from sz.api import response as sz_api_response
from sz.core import models, services
from sz.core.services import morphology, gis


categorization_service = morphology.CategorizationService(
    models.Category.objects.all(), morphology.RussianStemmingService())
city_service = gis.BlagoveshchenskCityService()
venue_service = None
place_service = services.PlaceService(city_service, None, categorization_service)


class SzApiView(APIView):
    """
        Base class for SZ Web API views
    """

    def handle_exception(self, exc):
        base_response = APIView.handle_exception(self, exc)
        return sz_api_response.Response(base_response.data, status=base_response.status_code)


class InvalidRequestException(Exception):
    pass


class FilteredListView(SzApiView):

    request_form_class = None

    request_form_errors = None

    def handle_exception(self, exc):
        if isinstance(exc, InvalidRequestException):
            return sz_api_response.Response(self.request_form_errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super(FilteredListView, self).handle_exception(exc)

    def get_request_params(self, request):
        request_form = self.request_form_class(request.QUERY_PARAMS)
        if request_form.is_valid():
            return request_form.cleaned_data
        else:
            self.request_form_errors = request_form.errors
            raise InvalidRequestException()


class ApiRoot(SzApiView):
    def get(self, request, format=None):
        return sz_api_response.Response({
            'city-nearest': reverse('city-nearest'),
            'categories': reverse('category-list'),
            'places-newsfeed': reverse('place-newsfeed'),
            'places-search': reverse('place-search'),
            'login': reverse('auth-login'),
            'logout': reverse('auth-logout'),
            'current-user': reverse('auth-user'),
            })