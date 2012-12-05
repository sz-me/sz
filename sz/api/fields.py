from rest_framework import fields
from sz.api import pagination
from sz.api import services

class NestedField(fields.Field):
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        self.paginate_by = kwargs.pop('paginate_by', None)
        assert self.serializer, 'serializer is required'
        super(NestedField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        """
        Converts the field's value into it's simple representation.
        """
        if fields.is_simple_callable(value):
            value = value()
        if issubclass(self.serializer, pagination.PaginationSerializer):
            if self.paginate_by:
                value = services.paginated_content(value, paginate_by=self.paginate_by)
            else:
                value = services.paginated_content(value)
        serializer = self.serializer(instance=value)
        return serializer.data

class ResourceField (fields.HyperlinkedIdentityField):
    def field_to_native(self, obj, field_name):
        url = super(ResourceField, self).field_to_native(obj, field_name)
        return { 'url': url, }