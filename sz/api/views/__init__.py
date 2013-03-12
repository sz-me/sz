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


class InvalidRequestException(Exception):

    def __init__(self, errors):
        self.errors = errors


class SzApiView(APIView):
    """
        Base class for SZ Web API views
    """

    def handle_exception(self, exc):
        if isinstance(exc, InvalidRequestException):
            return sz_api_response.Response(self.request_form_errors, status=status.HTTP_400_BAD_REQUEST)
        base_response = APIView.handle_exception(self, exc)
        return sz_api_response.Response(base_response.data, status=base_response.status_code)

    def validate_and_get_params(self, form_class, data=None, files=None):
        request_form = form_class(data=data, files=files)
        if request_form.is_valid():
            return request_form.cleaned_data
        else:
            self.request_form_errors = request_form.errors
            raise InvalidRequestException(request_form.errors)


class ApiRoot(SzApiView):
    def get(self, request, format=None):
        return sz_api_response.Response({
            'city-nearest': reverse('city-nearest', request=request),
            'categories': reverse('category-list', request=request),
            'places-newsfeed': reverse('place-newsfeed', request=request),
            'places-search': reverse('place-search', request=request),
            'places-venues-search': reverse('place-venue-search', request=request),
            'login': reverse('auth-login', request=request),
            'logout': reverse('auth-logout', request=request),
            'current-user': reverse('auth-user', request=request),
            'message-previews': reverse('message-preview-list', request=request),
            })