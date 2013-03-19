# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import permissions
from rest_framework.reverse import reverse
from sz.api import serializers, forms, response as sz_api_response
from sz.core import models
from sz.api.views import SzApiView, news_feed_service, place_service, message_service


class PlaceRootNews(SzApiView):
    """
    News feed that represents a list of places of whom somebody recently left a message
    For example, [news feed for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """

    def get(self, request, format=None):
        params = self.validate_and_get_params(forms.NewsRequestForm, request.QUERY_PARAMS)
        news_feed = news_feed_service.get_news(**params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedResponseBuilder(photo_host, request)
        serialized_news_feed = response_builder.build(news_feed)
        return sz_api_response.Response(serialized_news_feed)


class PlaceVenueSearch(SzApiView):
    """
    Wrapper for Venue search
    For example, [places for position (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def _serialize_item(self, item):
        item_serializer = serializers.PlaceSerializer(instance=item[u'place'])
        serialized_item = {"place": item_serializer.data, "distance": int(item["distance"])}
        return serialized_item

    def get(self, request, format=None):
        params = self.validate_and_get_params(forms.PlaceSearchRequestForm, request.QUERY_PARAMS)
        places = place_service.search_in_venues(**params)
        response = [self._serialize_item(place) for place in places]
        return sz_api_response.Response(response)


class PlaceSearch(SzApiView):
    """
    Place search
    For example, [places for position (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """

    def _serialize_item(self, item):
        item_serializer = serializers.PlaceSerializer(instance=item[u'place'])
        serialized_item = {
            "place": item_serializer.data, "distance": int(item["distance"]), "azimuth": int(item["azimuth"])
        }
        return serialized_item

    def get(self, request, format=None):
        params = self.validate_and_get_params(forms.PlaceSearchRequestForm, request.QUERY_PARAMS)
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


class PlaceInstanceNewsFeed(SzApiView):
    """
    Retrieve news feed item for a place instance.
    """

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        params = self.validate_and_get_params(forms.NewsRequestForm, request.QUERY_PARAMS)
        place = self.get_object(pk)
        news_feed_item = news_feed_service.get_place_news(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedItemResponseBuilder(photo_host, request)
        return sz_api_response.Response(response_builder.build(news_feed_item))


class PlaceInstanceMessages(SzApiView):

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        params = self.validate_and_get_params(forms.MessageRequestForm, request.QUERY_PARAMS)
        place = self.get_object(pk)
        messages = message_service.get_place_messages(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.PlaceMessagesResponseBuilder(photo_host, request)
        return sz_api_response.Response(response_builder.build(place, messages))
