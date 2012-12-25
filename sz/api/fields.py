from rest_framework import fields
from sz.api import pagination
from sz.api import services

class NestedField(fields.Field):
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        self.paginate_by = kwargs.pop('paginate_by', None)
        self.transform = kwargs.pop('transform', None)
        assert self.transform, 'transform is required'
        kwargs['source']='*'
        super(NestedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        """
        Converts the field's value into it's simple representation.
        """
        args = hasattr(self.parent, 'trans_args') and self.parent.trans_args or None
        value = self.transform(obj, args)
        if self.serializer:
            if issubclass(self.serializer, pagination.PaginationSerializer):
                if self.paginate_by:
                    value = services.paginated_content(value, paginate_by=self.paginate_by)
                else:
                    value = services.paginated_content(value)
            serializer = self.serializer(instance=value)
            value = serializer.data
        return value

class ResourceField (fields.HyperlinkedIdentityField):
    def field_to_native(self, obj, field_name):
        url = super(ResourceField, self).field_to_native(obj, field_name)
        return { 'url': url, }