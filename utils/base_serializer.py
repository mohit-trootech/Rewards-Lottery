from rest_framework import serializers


class DynamicModelSerializer(serializers.ModelSerializer):
    """
    Dynamic fields serializer to update child serializers fields based on query_params
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = kwargs.pop("fields", None)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
