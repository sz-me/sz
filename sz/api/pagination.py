# -*- coding: utf-8 -*-
from rest_framework import pagination
from rest_framework import serializers
from rest_framework.templatetags.rest_framework import replace_query_param

class NextPageField(serializers.Field):
    """
    Field that returns a link to the next page in paginated results.
    """
    page_field = 'page'

    def to_native(self, value):
        if not value.has_next():
            return None
        page = value.next_page_number()
        request = self.context.get('request')
        url = request and request.get_full_path() or ''
        return replace_query_param(url, self.page_field, page)


class PreviousPageField(serializers.Field):
    """
    Field that returns a link to the previous page in paginated results.
    """
    page_field = 'page'

    def to_native(self, value):
        if not value.has_previous():
            return None
        page = value.previous_page_number()
        request = self.context.get('request')
        url = request and request.get_full_path() or ''
        return replace_query_param(url, self.page_field, page)

class PaginationSerializer(pagination.BasePaginationSerializer):
    """
    A default implementation of a pagination serializer.
    """
    count = serializers.Field(source='paginator.count')
    next = NextPageField(source='*')
    previous = PreviousPageField(source='*')
