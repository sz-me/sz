# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from sz.api import pagination, fields as sz_api_fields
from sz.core import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source="username")
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ('username','full_name')


class AuthenticationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        user = self.serializer = kwargs.pop('user', None)
        self.trans_args = {'user': user}
        super(AuthenticationSerializer, self).__init__(*args, **kwargs)

    token = serializers.Field(source='key')
    user = sz_api_fields.NestedField(transform=lambda p, a: a.get('user', None), serializer=UserSerializer)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        exclude = ('keywords',)


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Message
        read_only_fields = ('date',)
        exclude = ('place', 'user', 'stems',)


class PaginatedMessageSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MessageSerializer


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    longitude = serializers.Field()
    latitude = serializers.Field()
    foursquare_details_url = serializers.Field()

    class Meta:
        model = models.Place
        exclude = ('messages', 'date', 'position', )
