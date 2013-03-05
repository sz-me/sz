# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import status
from rest_framework.reverse import reverse
from sz.core import models
from sz.api import serializers, response as sz_api_response, forms
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


class MessageInstancePhoto(SzApiView):
    """ Add or delete a photo. """

    def get_object(self, pk):
        try:
            return models.Message.objects.get(pk=pk)
        except models.Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        if not message.photo:
            raise Http404
        root_url = reverse('client-index', request=request)
        photo = message.get_photo_absolute_urls(root_url)
        return sz_api_response.Response(photo)

    def post(self, request, pk, format=None):
        params = self.validate_and_get_params(forms.AddPhotoForm, request.DATA, request.FILES)
        message = self.get_object(pk)
        if message.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        if message.photo:
            return sz_api_response.Response(status=status.HTTP_406_NOT_ACCEPTABLE, info="Already exist")
        print params['photo']
        message.photo = params['photo']
        message.save()
        root_url = reverse('client-index', request=request)
        photo = message.get_photo_absolute_urls(root_url)
        return sz_api_response.Response(photo)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        if message.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        if message.photo:
            message.reduced_photo.delete(save=False)
            message.thumbnail.delete(save=False)
            message.photo.delete(save=False)
            message.save()
        return sz_api_response.Response(status=status.HTTP_204_NO_CONTENT)