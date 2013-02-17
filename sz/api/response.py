# -*- coding: utf-8 -*-
from rest_framework.response import Response as RestFrameworkResponse

class Response(RestFrameworkResponse):
    """
    An HttpResponse that allows it's data to be rendered into
    arbitrary media types.
    """
    def __init__(self, data=None, status=200,
                 template_name=None, headers=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be defered,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status, template_name=template_name, headers=headers)
        self.data = {'data': data, 'meta': {'code': status}}


