# -*- coding: utf-8 -*-
from rest_framework import permissions
from sz.api.views import SzApiView
from sz.api import serializers, response as sz_api_response


class UserInstanceSelf(SzApiView):
    """ Retrieve profile information for the action user """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = serializers.UserSerializer(instance=user)
        return sz_api_response.Response(serializer.data)
