# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.reverse import reverse
from sz.core import models
from sz.api import serializers, response as sz_api_response, forms
from sz.api.views import SzApiView, categorization_service, message_service


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
        if message.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        if message.photo:
            message.reduced_photo.delete(save=False)
            message.thumbnail.delete(save=False)
            message.photo.delete(save=False)
            message.save()
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


class MessagePreviewRoot(SzApiView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        previews = models.MessagePreview.objects.filter(user=request.user)
        serializer = serializers.MessagePreviewSerializer(instance=previews)
        return sz_api_response.Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.MessagePreviewSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            message_preview = serializer.object
            message_preview.user = request.user
            message_preview.save()
            if message_preview.text is not None:
                if message_preview.text != '':
                    categories = categorization_service.detect_categories(message_preview.text)
                    message_preview.categories.clear()
                    for category in categories:
                        message_preview.categories.add(category)
                #categorization_service.assert_stems(message_preview)
            serialized_preview = serializers.MessagePreviewSerializer(instance=message_preview).data
            root_url = reverse('client-index', request=request)
            serialized_preview['photo'] = message_preview.get_photo_absolute_urls(root_url)
            return sz_api_response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagePreviewInstance(SzApiView):
    """ Retrieve or delete a message preview. """

    def get_object(self, pk):
        try:
            return models.MessagePreview.objects.get(pk=pk)
        except models.MessagePreview.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        if message_preview.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewSerializer(instance=message_preview)
        place_serializer = serializers.PlaceSerializer(instance=message_preview.place)
        data = serializer.data
        root_url = reverse('client-index', request=request)
        data['photo'] = message_preview.get_photo_absolute_urls(root_url)
        data['place'] = place_serializer.data
        return sz_api_response.Response(data)

    def delete(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        if message_preview.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        message_preview.delete()
        return sz_api_response.Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        if message_preview.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewSerializer(message_preview, data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return sz_api_response.Response(serializer.data)
        else:
            return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagePreviewInstancePublish(SzApiView):
    """ Publishes a message preview. """

    def get_object(self, pk):
        try:
            return models.MessagePreview.objects.get(pk=pk)
        except models.MessagePreview.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        if message_preview.user != request.user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewForPublicationSerializer(message_preview, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            message = models.Message(text=message_preview.text, photo=message_preview.photo,
                                     place=message_preview.place, smile=message_preview.smile,
                                     user=message_preview.user)
            message.save()
            for category in message_preview.categories.all():
                message.categories.add(category)
            message_preview.delete()
            categorization_service.assert_stems(message)
            message_serializer = serializers.MessageSerializer(instance=message)
            place_serializer = serializers.PlaceSerializer(instance=message.place)
            data = message_serializer.data
            root_url = reverse('client-index', request=request)
            data['photo'] = message.get_photo_absolute_urls(root_url)
            data['place'] = place_serializer.data
            return sz_api_response.Response(data)
        else:
            return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageRootSearch(SzApiView):
    """
    Message search for current location
    For example, [messages for position (50.2616113, 127.5266082)](?latitude=50.2616113&longitude=127.5266082).
    """
    def get(self, request, format=None):
        params = self.validate_and_get_params(forms.NewsRequestForm, request.QUERY_PARAMS)
        result = message_service.search(**params)
        root_url = reverse('client-index', request=request)
        response_builder = sz_api_response.SearchMessageResponseBuilder(root_url, request)
        data = response_builder.build(result)
        return sz_api_response.Response(data)

