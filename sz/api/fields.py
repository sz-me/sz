from rest_framework import fields

class NestedField(fields.Field):
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        assert self.serializer, 'serializer is required'
        super(NestedField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        """
        Converts the field's value into it's simple representation.
        """
        if fields.is_simple_callable(value):
            value = value()
        serializer = self.serializer(instance=value)
        return serializer.data