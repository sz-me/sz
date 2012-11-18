# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from sz.api import serializers
from sz.api import services as api_services
from sz.api.response import Response
from sz.core import models
from sz.core import services

class SzApiView(APIView):
    """
        Base class for SZ Web API views
    """
    def handle_exception(self, exc):
        base_response = APIView.handle_exception(self, exc)
        return Response(base_response.data, status = base_response.status_code)

class ApiRoot(SzApiView):
    def get(self, request, format=None):
        return Response({
            'messages': reverse('message-list', request=request),
            'cities': reverse('city-list', request=request),
            'places': reverse('place-list', request=request),
            'users': reverse('user-list', request=request),
            'things': reverse('thing-list', request=request),
            'categories': reverse('category-list', request=request),
        })

class MessageRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        messages = models.Message.objects.all()
        serializer = serializers.MessageSerializer(instance=messages)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            message = serializer.object
            message.user = request.user
            message.save()
            things = models.Thing.objects.all()
            categorization_service = services.CategorizationService()
            categorization_service.detect_thinks(things, message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageInstance(SzApiView):
    """
    Retrieve, update or delete a message instance.
    """

    def get_object(self, pk):
        try:
            return models.Message.objects.get(pk=pk)
        except models.Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = serializers.MessageSerializer(instance=message)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = serializers.MessageSerializer(data=request.DATA, instance=message)
        if serializer.is_valid():
            message = serializer.object
            message.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRoot(SzApiView):
    """
    List all users.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = serializers.UserSerializer(instance=users)
        return Response(serializer.data)


class CityRoot(SzApiView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        serializer = serializers.CitySearchSerializer(data=request.QUERY_PARAMS)
        if serializer.is_valid():
            position = {
                'latitude': request.QUERY_PARAMS.get('latitude'),
                'longitude': request.QUERY_PARAMS.get('longitude')
                }
            query = request.QUERY_PARAMS.get('query')
            return Response(api_services.geonames_city_service(position, query))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceRoot(SzApiView):
    """
    List of places near the current location.
    For example, [places near 50.2616113, 127.5266082](?latitude=50.2616113&longitude=127.5266082).
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        serializer = serializers.PlaceSearchSerializer(data=request.QUERY_PARAMS)
        if serializer.is_valid():
            position = {
                'latitude': request.QUERY_PARAMS['latitude'],
                'longitude': request.QUERY_PARAMS['longitude'],
                'accuracy': request.QUERY_PARAMS.get('accuracy'),
                }
            if request.QUERY_PARAMS.get('query'):
                query = u"%s" % request.QUERY_PARAMS['query']
            else:
                query = None
            places = api_services.venue_place_service(position, query)
            return Response(places)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThingRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        things = models.Thing.objects.all()
        serializer = serializers.ThingSerializer(instance=things)
        return Response(serializer.data)

class CategoryRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(instance=categories)
        return Response(serializer.data)