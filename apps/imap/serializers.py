from rest_framework import serializers

class FolderSerializer(serializers.Serializer):
    name = serializers.CharField()

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField()
    subject = serializers.CharField()
    from_address = serializers.CharField(source='from')
    date = serializers.CharField()
