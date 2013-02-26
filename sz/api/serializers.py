# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from sz.api import fields as sz_api_fields
from sz.core import models


class UserSerializer(serializers.ModelSerializer):
    absolute_url = serializers.Field(source='get_absolute_url')
    full_name = serializers.Field(source='get_full_name')

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions',)


class AuthUserSerializer(serializers.ModelSerializer):
    is_anonymous = serializers.Field()
    is_authenticated = serializers.Field()

    class Meta:
        model = User
        fields = ('username', 'is_anonymous', 'is_authenticated')



class AuthenticationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        user = self.serializer = kwargs.pop('user', None)
        self.trans_args = {'user': user}
        super(AuthenticationSerializer, self).__init__(*args, **kwargs)

    token = serializers.Field(source='key')
    user = sz_api_fields.NestedField(transform=lambda p, a: a.get('user', None), serializer=UserSerializer)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ('keywords',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        read_only_fields = ('date',)
        exclude = ('place', 'user', 'stems',)


class PlaceSerializer(serializers.ModelSerializer):
    longitude = serializers.Field()
    latitude = serializers.Field()
    foursquare_details_url = serializers.Field()

    class Meta:
        model = models.Place
        exclude = ('messages', 'date', 'position', 'photo')
