# -*- coding: utf-8 -*-
from rest_framework.response import Response as RestFrameworkResponse
from rest_framework.reverse import reverse
from sz.api import serializers


class Response(RestFrameworkResponse):
    """
    An HttpResponse that allows it's data to be rendered into
    arbitrary media types.
    """
    def __init__(self, data=None, status=200,
                 template_name=None, headers=None, info=dict()):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be defered,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status, template_name=template_name, headers=headers)
        self.data = {'data': data, 'meta': {'code': status, 'info': info}}


class FeedServiceResponseBuilder:
    def __init__(self, request=None):
        self.request = request

    def _convert_feed_service_result_to_response(self, result, items,
                                                 viewname, args=None, kwargs=None, format=None, **extra):
        params = result.get('params')
        if params.get('category', None) is not None:
            params['category'] = params.get('category').pk
        else:
            params['category'] = ""
        url = reverse(viewname, args, kwargs, request=self.request, format=format, **extra)
        return dict(url=url, params=result.get('params'), results=items,
                    count=result.get('count'))


class PlaceMessagesResponseBuilder(FeedServiceResponseBuilder):
    def __init__(self, photo_host_url="", request=None):
        self.photo_host_url = photo_host_url
        FeedServiceResponseBuilder.__init__(self, request)

    def build(self, place, messages):
        photos = [(message.id, message.get_photo_absolute_urls(self.photo_host_url))
                  for message in messages["items"]]
        photo_by_id = lambda id: filter(lambda p: p[0] == id, photos)[0][1]
        message_serializer = serializers.MessageSerializer(instance=messages["items"])
        serialized_messages = message_serializer.data
        for serialized_message in serialized_messages:
            serialized_message['photo'] = photo_by_id(serialized_message['id'])
        serialized_messages = self._convert_feed_service_result_to_response(
            messages, serialized_messages, 'place-detail-messages', (place.pk,))
        return serialized_messages


class NewsFeedItemResponseBuilder(FeedServiceResponseBuilder):
    def __init__(self, photo_host_url="", request=None):
        self.messages_response_builder = PlaceMessagesResponseBuilder(photo_host_url, request)
        FeedServiceResponseBuilder.__init__(self, request)

    def build(self, item):
        serialized_messages = self.messages_response_builder.build(item["place"], item["messages"])
        place_serializer = serializers.PlaceSerializer(instance=item["place"])
        serialized_item = dict(
            place=place_serializer.data, distance=int(item["distance"]),
            messages=serialized_messages)
        photos = item.get('photos', None)
        if photos is not None:
            serialized_photos = self.messages_response_builder.build(item["place"], photos)
            serialized_item['photos'] = serialized_photos
        return serialized_item


class NewsFeedResponseBuilder(FeedServiceResponseBuilder):
    def __init__(self, photo_host_url="", request=None):
        self.item_response_builder = NewsFeedItemResponseBuilder(photo_host_url, request)
        FeedServiceResponseBuilder.__init__(self, request)

    def build(self, feed):
        serialized_feed = self._convert_feed_service_result_to_response(
            feed, [self.item_response_builder.build(item) for item in feed['items']], 'place-news')
        return serialized_feed


class SearchMessageResponseBuilder(FeedServiceResponseBuilder):
    def __init__(self, photo_host_url="", request=None):
        self.photo_host_url = photo_host_url
        FeedServiceResponseBuilder.__init__(self, request)

    def __serialize_item(self, item):
        message_serializer = serializers.MessageSerializer(instance=item['message'])
        serialized_message = message_serializer.data
        serialized_message['photo'] = item['message'].get_photo_absolute_urls(self.photo_host_url)
        place_serializer = serializers.PlaceSerializer(instance=item['place'])
        serialized_place = place_serializer.data
        return dict(message=serialized_message, place=serialized_place, distance=int(item['distance']))

    def build(self, items):
        serialized_items = self._convert_feed_service_result_to_response(
            items, [self.__serialize_item(item) for item in items['items']], 'message-search')
        return serialized_items
