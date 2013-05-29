# -*- coding: utf-8 -*-
from rest_framework import permissions, status

from sz.api import serializers
from sz.api.response import Response
from sz.api.serializers import AuthUserSerializer, \
    RegistrationSerializer, ResendingConfirmationKeySerializer
from sz.api.views import SzApiView


class UsersRoot(SzApiView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            user_serializer = AuthUserSerializer(instance=user)
            return Response(user_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersRootResendingActivationKey(SzApiView):
    """ Sends an email with a confirmation key """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResendingConfirmationKeySerializer(
            data=request.DATA
        )
        if serializer.is_valid():
            return Response({})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserInstanceSelf(SzApiView):
    """ Retrieve profile information for the action user """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = serializers.UserSerializer(instance=user)
        return Response(serializer.data)
