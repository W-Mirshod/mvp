from rest_framework import serializers

class SpamDetectionInputSerializer(serializers.Serializer):
    email_content = serializers.CharField(required=True, max_length=100000)