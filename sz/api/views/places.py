# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from sz.api import serializers, forms, response as sz_api_response
from sz.core import models
from sz.api.views import SzApiView, FilteredListView, place_service, categorization_service


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
