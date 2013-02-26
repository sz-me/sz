# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.authtoken import models as authtoken_models
from rest_framework.authtoken import serializers as authtoken_serializers
from sz.api import serializers, forms, response as sz_api_response
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
            'users': reverse('user-list'),
        })


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


class MessageInstance(SzApiView):
    """ Retrieve or delete a message. """

    def get_object(self, pk):
        try:
            return models.Message.objects.get(pk=pk)
        except models.Message.DoesNotExist:
            raise Http404 #return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = serializers.MessageSerializer(instance=message)
        data = serializer.data
        root_url = reverse('client-index', request=request)
        data['photo'] = message.get_photo_absolute_urls(root_url)
        return sz_api_response.Response(serializer.data)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        if message.user == request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return sz_api_response.Response(status=status.HTTP_204_NO_CONTENT)


class UserInstanceSelf(SzApiView):
    """ Retrieve profile information for the action user """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        serializer = serializers.UserSerializer(instance=user)
        return sz_api_response.Response(serializer.data)
    

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


class PlaceRootNewsFeed(FilteredListView):
    """
    News feed that represents a list of places of whom somebody recently left a message
    For example, [news feed for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """

    request_form_class = forms.NewsFeedRequestForm

    def get(self, request, format=None):
        params = self.get_request_params(request)
        news_feed = place_service.get_news_feed(**params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedResponseBuilder(photo_host)
        serialized_news_feed = response_builder.build(news_feed)
        return sz_api_response.Response(serialized_news_feed)


class PlaceSearch(FilteredListView):
    """
    Wrapper for Venue search
    For example, [places for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """
    permission_classes = (permissions.IsAuthenticated,)
    request_form_class = forms.PlaceSearchRequestForm

    def _serialize_item(self, item):
        item_serializer = serializers.PlaceSerializer(instance=item[u'place'])
        serialized_item = {"place": item_serializer.data, "distance": item["distance"]}
        return serialized_item

    def get(self, request, format=None):
        params = self.get_request_params(request)
        places = place_service.search(**params)
        response = [self._serialize_item(place) for place in places]
        return sz_api_response.Response(response)


class PlaceInstance(SzApiView):
    """
    Retrieve a place instance.
    """

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = serializers.PlaceSerializer(instance=place)
        return sz_api_response.Response(serializer.data)


class PlaceInstanceNewsFeed(FilteredListView):
    """
    Retrieve news feed item for a place instance.
    """

    request_form_class = forms.NewsFeedRequestForm

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        params = self.get_request_params(request)
        place = self.get_object(pk)
        news_feed_item = place_service.get_place_news_feed(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedItemResponseBuilder(photo_host)
        return sz_api_response.Response(response_builder.build(news_feed_item))


class PlaceInstanceMessages(FilteredListView):

    request_form_class = forms.MessageRequestForm

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Place.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        print 'POST'
        serializer = serializers.MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            message = serializer.object
            message.place = models.Place.objects.get(pk=pk)
            print message.place
            message.user = request.user
            print message.user
            message.save()
            categorization_service.assert_stems(message)
            return sz_api_response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        params = self.get_request_params(request)
        place = self.get_object(pk)
        messages = place_service.get_place_messages(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.PlaceMessagesResponseBuilder(photo_host)
        return sz_api_response.Response(response_builder.build(place, messages))


class Authentication(SzApiView):
    model = authtoken_models.Token

    def get(self, request):
        responseSerializer = serializers.AuthenticationSerializer(
            instance=request.auth, user=request.user)
        return sz_api_response.Response(responseSerializer.data)

    def post(self, request):
        serializer = authtoken_serializers.AuthTokenSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = authtoken_models.Token.objects.get_or_create(user=user)
            responseSerializer = serializers.AuthenticationSerializer(instance=token, user=user)
            return sz_api_response.Response(responseSerializer.data)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
