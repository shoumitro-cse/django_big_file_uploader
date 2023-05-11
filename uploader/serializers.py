from rest_framework import serializers


class UploaderSerializer(serializers.Serializer):
    file = serializers.FileField()
    filename = serializers.CharField()
    storage_path = serializers.CharField()
    is_end = serializers.BooleanField()
