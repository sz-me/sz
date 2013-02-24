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


class FeedResponseBuilderBase:
    def _convert_feed_service_result_to_response(self, result, url, items):
        params = result.get('params')
        if result.get('category') is not None:
            params['category'] = result.get('category').pk
        else:
            params['category'] = ""
        return dict(url=url, params=result.get('params'), results=items,
                    count=result.get('count'))


class FeedItemResponseBuilder(FeedResponseBuilderBase):
    def __init__(self, photo_host_url=""):
        self.photo_host_url = photo_host_url

    def build(self, item):
        place_serializer = serializers.PlaceSerializer(instance=item["place"])
        photos = [(message.id, message.get_photo_absolute_urls(self.photo_host_url))
                  for message in item["messages"]["items"]]
        photo_by_id = lambda id: filter(lambda p: p[0] == id, photos)[0][1]
        message_serializer = serializers.MessageSerializer(instance=item["messages"]["items"])
        serialized_messages = message_serializer.data
        for serialized_message in serialized_messages:
            serialized_message['photo'] = photo_by_id(serialized_message['id'])
        serialized_item = dict(
            place=place_serializer.data, distance=item["distance"],
            messages=self._convert_feed_service_result_to_response(
                item["messages"], reverse('place-messages', (item["place"].pk,)), serialized_messages))
        return serialized_item


class FeedResponseBuilder(FeedResponseBuilderBase):
    def __init__(self, photo_host_url=""):
        self.item_response_builder = FeedItemResponseBuilder(photo_host_url)

    def build(self, feed):
        serialized_feed = self._convert_feed_service_result_to_response(
            feed, reverse('place-feed'), [self.item_response_builder.build(item) for item in feed['items']])
        return serialized_feed



