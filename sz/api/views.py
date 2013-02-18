# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from sz.api import serializers, services as api_services, forms
from sz.api.response import Response
from sz.core import models, services, queries
from sz.core.services import morphology, gis
from rest_framework.authtoken import models as authtoken_models
from rest_framework.authtoken import serializers as authtoken_serializers

categorization_service = morphology.CategorizationService(
    models.Category.objects.all(),
    morphology.RussianStemmingService())
city_service = gis.BlagoveshchenskCityService()
venue_service = None
place_service = services.PlaceService(city_service, None, categorization_service)


class SzApiView(APIView):
    """
        Base class for SZ Web API views
    """
    def handle_exception(self, exc):
        base_response = APIView.handle_exception(self, exc)
        return Response(base_response.data, status = base_response.status_code)

    paginate_by = 2

    def _get_list(self, queryset, request, paginated_serializer):
        page = request.QUERY_PARAMS.get('page')
        data = api_services.paginated_content(queryset, page, self.paginate_by)
        serializer_context = {'request': request}
        serializer = paginated_serializer(data, context=serializer_context)
        list = serializer.data
        return list


class ApiRoot(SzApiView):

    def get(self, request, format=None):
        return Response({
            'city-nearest': reverse('city-nearest'),
            'categories': reverse('category-list'),
            'places-feed': reverse('place-feed'),
            'users': reverse('user-list'),
        })


class CategoriesRoot(SzApiView):
    """ List of available categories of clothes """

    def get(self, request, format=None):
        categories = categorization_service.get_categories()
        serializer = serializers.CategorySerializer(instance=categories)
        return Response(serializer.data)


class CategoriesDetect(SzApiView):
    """ Detect categories of clothes in a text """

    def get(self, request, format=None):
        categories_detecting_request_form = forms.CategoriesDetectingRequestForm(request.QUERY_PARAMS)
        if categories_detecting_request_form.is_valid():
            params = categories_detecting_request_form.cleaned_data
            categories = categorization_service.detect_categories(params['text'])
            serializer = serializers.CategorySerializer(instance=categories)
            return Response(serializer.data)
        else:
            return Response(categories_detecting_request_form.errors)


class CategoriesInstance(SzApiView):
    """ Retrieve a category of clothes """

    def get(self, request, pk, format=None):
        categories = categorization_service.get_categories()
        filtered_categories = filter(lambda c: ("%s" % c.pk) == pk, categories)
        if len(filtered_categories) == 0:
            filtered_categories = filter(lambda c: c.alias == pk, categories)
        if len(filtered_categories) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CategorySerializer(instance=filtered_categories[0])
        return Response(serializer.data)


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
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        if message.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRoot(SzApiView):
    """ List all users. """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = serializers.UserSerializer(instance=users)
        return Response(serializer.data)


class CityNearest(SzApiView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        nearest_city_request = forms.NearestCityRequestForm(request.QUERY_PARAMS)
        if nearest_city_request.is_valid():
            params = nearest_city_request.cleaned_data
            response = city_service.get_city_by_position(params['longitude'], params['latitude'])
            return Response(response)
        else:
            return Response(nearest_city_request.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceFeed(SzApiView):
    """
    News feed that represents a list of places of whom somebody recently left a message
    For example, [news feed for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """
    def _serialize_item(self, item):
        place_serializer = serializers.PlaceSerializer(instance=item["place"])
        message_serializer = serializers.MessageSerializer(instance=item["messages"])
        serialized_item = {"place": place_serializer.data, "distance": item["distance"],
                           "messages": message_serializer.data}
        return serialized_item

    def get(self, request, format=None):
        feed_request = forms.FeedRequestForm(request.QUERY_PARAMS)
        if feed_request.is_valid():
            params = feed_request.cleaned_data
            feed = place_service.feed(**params)
            response = [self._serialize_item(item) for item in feed]
            return Response(response)
        else:
            return Response(feed_request.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceSearch(SzApiView):
    """
    Wrapper for Venue search
    For example, [places for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _serialize_item(self, item):
        item_serializer = serializers.PlaceSerializer(instance=item[u'place'])
        serialized_item = {"place": item_serializer.data, "distance": item["distance"]}
        return serialized_item

    def get(self, request, format=None):
        place_search_request = forms.PlaceSearchRequestForm(request.QUERY_PARAMS)
        if place_search_request.is_valid():
            params = place_search_request.cleaned_data
            places = place_service.search(**params)
            response = [self._serialize_item(place) for place in places]
            return Response(response)
        else:
            return Response(place_search_request.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data)


class PlaceMessages(SzApiView):
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
            categorization_service.detect_things(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Authentication(SzApiView):
    model = authtoken_models.Token
    def get(self, request):
        responseSerializer = serializers.AuthenticationSerializer(
            instance=request.auth, user=request.user)
        return Response(responseSerializer.data)
    def post(self, request):
        serializer = authtoken_serializers.AuthTokenSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = authtoken_models.Token.objects.get_or_create(user=user)
            responseSerializer = serializers.AuthenticationSerializer(instance=token, user=user)
            return Response(responseSerializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
