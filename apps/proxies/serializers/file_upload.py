from rest_framework import serializers


class TextFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
