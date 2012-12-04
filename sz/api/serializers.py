# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from sz.core import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)

from sz.api import fields as sz_api_fields
class ThingSerializer(serializers.ModelSerializer):
    category = sz_api_fields.NestedField(source='category', serializer=CategorySerializer)
    class Meta:
        model = models.Thing
        fields = ('tag', 'category')



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
            raise serializers.ValidationError("Latitude and longitude or query required")
        return attrs
