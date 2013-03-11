# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from sz.api import serializers, forms, response as sz_api_response
from sz.core import models
from sz.api.views import SzApiView, place_service, categorization_service


class PlaceRootNewsFeed(SzApiView):
    """
    News feed that represents a list of places of whom somebody recently left a message
    For example, [news feed for location (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """

    def get(self, request, format=None):
        params = self.validate_and_get_params(forms.NewsFeedRequestForm, request.QUERY_PARAMS)
        news_feed = place_service.get_news_feed(**params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedResponseBuilder(photo_host)
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
        places = place_service.venue_search(**params)
        response = [self._serialize_item(place) for place in places]
        return sz_api_response.Response(response)


class PlaceSearch(SzApiView):
    """
    Place search
    For example, [places for position (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """

    def _serialize_item(self, item):
        item_serializer = serializers.PlaceSerializer(instance=item[u'place'])
        serialized_item = {"place": item_serializer.data, "distance": int(item["distance"])}
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
        params = self.validate_and_get_params(forms.NewsFeedRequestForm, request.QUERY_PARAMS)
        place = self.get_object(pk)
        news_feed_item = place_service.get_place_news_feed(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.NewsFeedItemResponseBuilder(photo_host)
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
        messages = place_service.get_place_messages(place, **params)
        photo_host = reverse('client-index', request=request)
        response_builder = sz_api_response.PlaceMessagesResponseBuilder(photo_host)
        return sz_api_response.Response(response_builder.build(place, messages))


class PlaceInstanceMessagePreview(SzApiView):

    def post(self, request, pk, format=None):
        serializer = serializers.MessagePreviewSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            message_preview = serializer.object
            message_preview.place = models.Place.objects.get(pk=pk)
            message_preview.user = request.user
            message_preview.save()
            if message_preview.text is not None:
                if message_preview.text != '':
                    categories = categorization_service.detect_categories(message_preview.text)
                    message_preview.categories.clear()
                    for category in categories:
                        message_preview.categories.add(category)
            #categorization_service.assert_stems(message_preview)
            return sz_api_response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
