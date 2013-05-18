# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django.middleware import csrf
from rest_framework import permissions, status

from sz.api.serializers import AuthRequestSerializer, AuthUserSerializer
from sz.api.response import Response
from sz.api.views import SzApiView


class AuthLogin(SzApiView):
    """ Log a user in """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthRequestSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            auth.login(request, user)
            user_serializer = AuthUserSerializer(instance=user)
            csrf.get_token(request)
            return Response(user_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLogout(SzApiView):
    """ Log out a user who has been logged """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        auth.logout(request)
        user = auth_models.AnonymousUser()
        serializer = AuthUserSerializer(instance=user)
        return Response(serializer.data)


class AuthUser(SzApiView):
    """ Retrieve authentication information for the action user """

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        user = request.user
        serializer = AuthUserSerializer(instance=user)
        csrf.get_token(request)
        return Response(serializer.data)

"""
class Authentication(SzApiView):
    model = authtoken_models.Token

    def get(self, request):
        responseSerializer = serializers.AuthenticationSerializer(
            instance=request.auth, user=request.user)
        return sz_api_response.Response(responseSerializer.data)

    def post(self, request):
        serializer = authtoken_serializers.AuthTokenSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = authtoken_models.Token.objects.get_or_create(user=user)
            responseSerializer = serializers.AuthenticationSerializer(instance=token, user=user)
            return sz_api_response.Response(responseSerializer.data)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
