# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import status
from rest_framework.reverse import reverse
from sz.core import models
from sz.api import serializers, response as sz_api_response
from sz.api.views import SzApiView


class MessageInstance(SzApiView):
    """ Retrieve or delete a message. """

    def get_object(self, pk):
        try:
            return models.Message.objects.get(pk=pk)
        except models.Message.DoesNotExist:
            raise Http404

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
