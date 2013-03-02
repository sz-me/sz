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
        place_serializer = serializers.PlaceSerializer(instance=message.place)
        data = serializer.data
        root_url = reverse('client-index', request=request)
        data['photo'] = message.get_photo_absolute_urls(root_url)
        data['place'] = place_serializer.data
        return sz_api_response.Response(data)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        if message.user == request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return sz_api_response.Response(status=status.HTTP_204_NO_CONTENT)


class MessageResumes(SzApiView):
    """ List of available choices to resume a visit """

    def get(self, request, format=None):
        response = [dict(value=choice[0], name=choice[1]) for choice in models.VISIT_RESUME_CHOICES]
        return sz_api_response.Response(response)