# -*- coding: utf-8 -*-
import datetime, exceptions
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from sz.api import serializers, services as api_services
from sz.api.response import Response
from sz.core import lists, models, services, queries, utilities

class SzApiView(APIView):
    """
        Base class for SZ Web API views
    """
    def handle_exception(self, exc):
        base_response = APIView.handle_exception(self, exc)
        return Response(base_response.data, status = base_response.status_code)

    paginate_by = 2

    def _get_list(self, queryset, request, paginated_serializer):
        page = request.QUERY_PARAMS.get('page')
        data = api_services.paginated_content(queryset, page, self.paginate_by)
        serializer_context = {'request': request}
        serializer = paginated_serializer(data, context=serializer_context)
        list = serializer.data
        return list

class ApiRoot(SzApiView):
    def get(self, request, format=None):
        return Response({
            'messages': reverse('message-list'),
            'cities': reverse('city-list'),
            'places': reverse('place-list'),
            'users': reverse('user-list'),
            #'things': reverse('thing-list'),
            'categories': reverse('category-list'),
        })

class MessageRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        queryset = models.Message.objects.order_by('date').all()
        list_serializer = serializers.PaginatedMessageSerializer
        list = self._get_list(queryset, request, list_serializer)
        return Response(list)

    def post(self, request, format=None):
        print request.DATA
        serializer = serializers.MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            message = serializer.object
            print message
            message.user = request.user
            print message.user
            message.save()
            print "message.save() OK"
            things = models.Thing.objects.all()
            categorization_service = services.CategorizationService()
            categorization_service.detect_things(things, message)
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
            query = request.QUERY_PARAMS.get('place') and \
                     u"%s" % request.QUERY_PARAMS['place'] or None
            message = request.QUERY_PARAMS.get('message')
            nearby = request.QUERY_PARAMS.get('nearby')
            nearby = utilities.safe_cast(nearby, int, nearby)
            if message is None:
                places_from_venue = api_services.venue_place_service(position, query, nearby)
                places = [r['place'] for r in places_from_venue]
                if places:
                    if len(places) > 0:
                        caching_service = services.ModelCachingService(
                            places, lambda e: e.date, datetime.timedelta(seconds=60*60*24*7))
                        #print 'INSERT: ' + ', '.join([u'%s' % e for e in caching_service.for_insert])
                        #print 'UPDATE: ' + ', '.join([u'%s' % e for e in caching_service.for_update])
                        if len(caching_service.for_insert):
                            city_id = api_services.geonames_city_service(position)[0]['id']
                            for e in caching_service.for_insert:
                                e.city_id = city_id
                        if len(caching_service.cached) > 0:
                            for e in caching_service.cached:
                                stored_city = lists.first_match(
                                    lambda x: x.id == e.id,
                                    caching_service.stored)
                                e.city_id = stored_city.city_id
                        caching_service.save()
            else:
                city_id = api_services.geonames_city_service(position)[0]['id']
                places = queries.feed( \
                    latitude=position['latitude'],\
                    longitude=position['longitude'],\
                    city_id=city_id, nearby=nearby)
            serializer = serializers.PlaceSerializer(instance=places)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaceInstance(SzApiView):
    """
    Retrieve a place instance.
    """

    def get_object(self, pk):
        try:
            return models.Place.objects.get(pk=pk)
        except models.Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = serializers.PlaceSerializer(instance=place)
        return Response(serializer.data)

class ThingRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        things = models.Thing.objects.all()
        serializer = serializers.ThingSerializer(instance=things)
        return Response(serializer.data)

class ThingInstance(SzApiView):
    def get_object(self, pk):
        try:
            return models.Thing.objects.get(pk=pk)
        except models.Thing.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        thing = self.get_object(pk)
        serializer = serializers.ThingSerializer(instance=thing)
        return Response(serializer.data)

class ThingMessages(SzApiView):
    def get_object(self, pk):
        try:
            return models.Thing.objects.get(pk=pk)
        except models.Thing.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        messages = self.get_object(pk).message_set.all()
        serializer = serializers.MessageSerializer(instance=messages)
        return Response(serializer.data)

class CategoryRoot(SzApiView):
    """
    List all messages, or create a new message.
    """
    paginate_by = 4
    def get(self, request, format=None):
        queryset = models.Category.objects.all()
        list_serializer = serializers.PaginatedCategorySerializer
        list = self._get_list(queryset, request, list_serializer)
        return Response(list)