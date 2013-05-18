# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from sz.api import fields as sz_api_fields
from sz.core import models
from sz.core.services.users import RegistrationService

class UserSerializer(serializers.ModelSerializer):
    absolute_url = serializers.Field(source='get_absolute_url')
    full_name = serializers.Field(source='get_full_name')

    class Meta:
        model = models.User
        exclude = ('password', 'groups', 'user_permissions',)


class AuthUserEmail(serializers.EmailField):
    def field_to_native(self, obj, field_name):
        if isinstance(obj, AnonymousUser):
            field_name = 'username'
        return super(AuthUserEmail, self).field_to_native(obj, field_name)


class AuthUserSerializer(serializers.ModelSerializer):
    email = AuthUserEmail()
    is_anonymous = serializers.Field()
    is_authenticated = serializers.Field()

    class Meta:
        model = models.User
        fields = ('email', 'is_anonymous', 'is_authenticated')


class AuthenticationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        user = self.serializer = kwargs.pop('user', None)
        self.trans_args = {'user': user}
        super(AuthenticationSerializer, self).__init__(*args, **kwargs)

    token = serializers.Field(source='key')
    user = sz_api_fields.NestedField(transform=lambda p, a: a.get('user', None), serializer=UserSerializer)


class AuthRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password" fields')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ('keywords',)


class MessageBaseSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, blank=True)

    class Meta:
        read_only_fields = ('date',)
        exclude = ('place', 'user', 'stems',)

    def validate(self, attrs):
        """
        Check that the start is before the stop.
        """
        text = attrs.get('text', None)
        if text is None:
            text = ''
        else:
            text = attrs['text'].strip()
        photo = attrs.get('photo', None)
        if not (photo or text != ""):
            raise serializers.ValidationError("Message don't must be empty")
        return attrs


class MessageSerializer(MessageBaseSerializer):

    class Meta:
        model = models.Message
        read_only_fields = ('date',)
        exclude = ('place', 'user', 'stems',)


class MessagePreviewSerializer(MessageBaseSerializer):

    class Meta:
        model = models.MessagePreview
        exclude = ('user',)


class MessagePreviewForPublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MessagePreview
        fields = ('categories',)


class PlaceSerializer(serializers.ModelSerializer):
    longitude = serializers.Field()
    latitude = serializers.Field()
    foursquare_details_url = serializers.Field()

    class Meta:
        model = models.Place
        exclude = ('messages', 'date', 'position', 'photo')


class RegistrationSerializer(serializers.Serializer):
    registration_service = RegistrationService()

    email = serializers.EmailField(required=True)
    style = serializers.ChoiceField(required=True, choices=[
        (style.pk, style.name) for style in models.Style.objects.all()
    ])
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate_email(self, attrs, source):
        """
        Check that the blog post is about Django.
        """
        email = attrs[source]
        if models.User.objects.filter(email=email).count() > 0:
            raise serializers.ValidationError(_("Email is already used"))
        return attrs

    def validate(self, attrs):
        attrs = super(RegistrationSerializer, self).validate(attrs)
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise serializers.ValidationError(_("Passwords don\'t match"))

        style = models.Style.objects.get(pk=attrs.get('style'))
        user = self.registration_service.register(
            attrs.get('email'),
            style, password1
        )
        attrs['user'] = user
        return attrs
