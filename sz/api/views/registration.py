# -*- coding: utf-8 -*-
from rest_framework import status, permissions

from sz.api.views import SzApiView
from sz.api.response import Response
from sz.api.serializers import AuthUserSerializer, \
    RegistrationSerializer, ResendingConfirmationKeySerializer


class Registration(SzApiView):
    """ Registers an user """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            user_serializer = AuthUserSerializer(instance=user)
            return Response(user_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationResendingKey(SzApiView):
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

