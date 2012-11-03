# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from sz.api import serializers
from sz.api import services
from sz.api.response import Response
from sz.core.models import Message

class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'messages': reverse('message-list', request=request),
            'cities': reverse('city-list', request=request),
            'places': reverse('place-list', request=request),
            'users': reverse('user-list', request=request),

            })


class MessageRoot(APIView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = serializers.MessageSerializer(instance=messages)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.MessageSerializer(request.DATA)
        if serializer.is_valid():
            comment = serializer.object
            comment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageInstance(APIView):
    """
    Retrieve, update or delete a message instance.
    """

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = serializers.MessageSerializer(instance=message)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = serializers.MessageSerializer(request.DATA, instance=message)
        if serializer.is_valid():
            message = serializer.object
            message.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRoot(APIView):
    """
    List all users.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = serializers.UserSerializer(instance=users)
        return Response(serializer.data)

class CityRoot(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        serializer = serializers.CitySearchSerializer(request.QUERY_PARAMS)
        if serializer.is_valid():
            position = {
                'latitude': request.QUERY_PARAMS.get('latitude'),
                'longitude': request.QUERY_PARAMS.get('longitude')
                }
            query = request.QUERY_PARAMS.get('query')
            return Response(services.geonames_city_service(position, query))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaceRoot(APIView):
    """
    List of places near the current location.
    For example, [places near 50.2616113, 127.5266082](?latitude=50.2616113&longitude=127.5266082).
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        serializer = serializers.PlaceSearchSerializer(request.QUERY_PARAMS)
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
            places = services.venue_place_service(position, query)
            return Response(places)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
def tags(request):
    message = request.POST.get('message')
    tags = DomainTag.objects.all().order_by('-name')
    tags = services.spellcorrector_tagging_service(message, tags)
    return HttpResponse(simplejson.dumps({"tags": tags}, ensure_ascii=False), mimetype="application/json")
'''