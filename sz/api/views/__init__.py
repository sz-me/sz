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
message_service = services.MessageService(city_service, categorization_service)
news_feed_service = services.NewsFeedService(message_service)
place_service = services.PlaceService(city_service)


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
            'places-news': reverse('place-news', request=request),
            'places-search': reverse('place-search', request=request),
            'places-search-in-venues': reverse('place-search-in-venues', request=request),
            'login': reverse('auth-login', request=request),
            'logout': reverse('auth-logout', request=request),
            'current-user': reverse('auth-user', request=request),
            'messages-previews': reverse('message-preview-list', request=request),
            'messages-search': reverse('message-search', request=request),
            'users-registration': reverse('users-registration', request=request),
            'users-resending-activation-key': reverse('users-resending-activation-key', request=request),
            'users-profile': reverse('users-profile', request=request),
        })

