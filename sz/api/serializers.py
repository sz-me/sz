# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework import serializers
from sz.core import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class MessageSerializer(serializers.ModelSerializer):
    #categories
    class Meta:
        model = models.Message
        read_only_fields = ('date', )
        exclude = ('id', 'things', 'user',)

class PaginatedMessageSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of message querysets.
    """
    class Meta:
        object_serializer_class = MessageSerializer

class ThingSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.CharField(source='tag')
    messages = serializers.HyperlinkedIdentityField(view_name='thing-messages')
    class Meta:
        model = models.Thing
        fields = ('url', 'tag', 'messages')

class CategorySerializer(serializers.ModelSerializer):
    messages = serializers.HyperlinkedIdentityField(view_name='category-messages')
    class Meta:
        model = models.Category
        read_only_fields = ('name',)
        fields = ('name', 'messages')

class PlaceSearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required = True)
    longitude = serializers.FloatField(required = True)
    accuracy = serializers.FloatField(required = False)
    query = serializers.CharField(required = False)


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