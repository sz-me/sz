# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from sz.api import pagination, fields as sz_api_fields
from sz.core import models, gis, queries
from rest_framework.reverse import reverse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source="username")
    full_name = serializers.CharField(source="get_full_name")
    class Meta:
        model = User
        fields = ('username','full_name')

class MessageSerializer(serializers.ModelSerializer):
    username = sz_api_fields.NestedField(transform=lambda obj, args: obj.user.username)
    class Meta:
        model = models.Message
        read_only_fields = ('date', )
        exclude = ('place','user',)
class PaginatedMessageSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MessageSerializer

class CategorySerializer(serializers.Serializer):
    name = sz_api_fields.NestedField(transform=lambda obj, args: obj['name'])
    count = sz_api_fields.NestedField(transform=lambda obj, args: obj['count'])
    last = sz_api_fields.NestedField(transform=lambda obj, args: obj['last'])
    #messages = sz_api_fields.NestedField(serializer=MessageSerializer)

class PlaceSearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required = True)
    longitude = serializers.FloatField(required = True)
    accuracy = serializers.FloatField(required = False)
    place = serializers.CharField(required = False)
    message = serializers.CharField(required = False)
    nearby = serializers.IntegerField(required = False)

class PlaceSerializer(serializers.Serializer):
    """
    Формирует ответ на запрос ленты событий
    """
    def __init__(self, *args, **kwargs):
        longitude = self.serializer = kwargs.pop('longitude', None)
        latitude = self.serializer = kwargs.pop('latitude', None)
        assert longitude and latitude, 'longitude and latitude are required'
        position = gis.ll_to_point (longitude, latitude)
        messages = kwargs.pop('messages', [])
        things = kwargs.pop('things', None)
        stems = kwargs.pop('stems', None)
        request = kwargs.pop('request', None)
        self.trans_args = {
            'position' : position,
            'messages': messages,
            'things': things,
            'stems': stems,
            'request': request
        }
        super(PlaceSerializer, self).__init__(*args, **kwargs)
    url = serializers.HyperlinkedIdentityField(view_name='place-detail')
    name = serializers.CharField(max_length=128)
    address = serializers.CharField(max_length=128)
    crossStreet = serializers.CharField(max_length=128)
    contact = serializers.CharField(max_length=512)
    position = serializers.Field()
    city_id = serializers.IntegerField()
    shmotzhmot_details_url = sz_api_fields.NestedField(transform=lambda p, a:
        reverse('feed-place', kwargs={'id': p.id}, request=a.get('request', None)))
    foursquare_details_url = serializers.Field()
    foursquare_icon_prefix = serializers.Field()
    foursquare_icon_suffix = serializers.Field()
    distance = sz_api_fields.NestedField(transform=lambda p, a:
        gis.calculate_distance_p(p.position, a['position']))
    messages = sz_api_fields.NestedField(
        transform=lambda p, a: a['messages'](p, a),
        serializer=PaginatedMessageSerializer)

    categories = sz_api_fields.NestedField(
        transform=lambda obj, args: queries.categories(obj), serializer=CategorySerializer)

    class Meta:
        model = models.Place
        exclude = ('date',)

class CitySearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required = False)
    longitude = serializers.FloatField(required = False)
    query = serializers.CharField(required = False)

    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        query = attrs.get('query')
        if  not (latitude and longitude and not query or not latitude and not longitude and query):
            raise serializers.ValidationError("Only latitude and longitude or only query required")
        return attrs

class AuthenticationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        user = self.serializer = kwargs.pop('user', None)
        self.trans_args = {
            'user' : user,
        }
        super(AuthenticationSerializer, self).__init__(*args, **kwargs)

    token = serializers.Field(source='key')
    user = sz_api_fields.NestedField(transform=lambda p, a: a.get('user', None), serializer=UserSerializer)