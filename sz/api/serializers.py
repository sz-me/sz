# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from sz.api import pagination
from sz.core import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    #categories
    class Meta:
        model = models.Message
        read_only_fields = ('date', )
        exclude = ('things', 'user',)
class PaginatedMessageSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MessageSerializer

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='name')
    messages = serializers.HyperlinkedIdentityField(view_name='category-messages')
    class Meta:
        model = models.Category
class PaginatedCategorySerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CategorySerializer

from sz.api import fields as sz_api_fields
class ThingSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.CharField(source='tag')
    messages = sz_api_fields.ResourceField(view_name='thing-messages')
    category = sz_api_fields.NestedField(source='category', serializer=CategorySerializer)
    class Meta:
        model = models.Thing
        fields = ('url', 'tag', 'category', 'messages')

class PlaceSearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required = True)
    longitude = serializers.FloatField(required = True)
    accuracy = serializers.FloatField(required = False)
    place = serializers.CharField(required = False)
    message = serializers.CharField(required = False)
    nearby = serializers.IntegerField(required = False)
class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    #distance = serializers.Field(source='*')
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    foursquare_details_url = serializers.Field()
    messages = sz_api_fields.NestedField(source='all_messages', serializer=PaginatedMessageSerializer)
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