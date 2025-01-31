from rest_framework import serializers

class SpamDetectionInputSerializer(serializers.Serializer):
    email_content = serializers.CharField(required=True, max_length=100000)

class EmailInputSerializer(serializers.Serializer):
    email_body = serializers.CharField()

class EmailThemeSerializer(serializers.Serializer):
    theme = serializers.CharField()

class EmailPersonalizationInputSerializer(serializers.Serializer):
    email_body = serializers.CharField(required=True, help_text="The content of the email to personalize")
    theme = serializers.CharField(required=True, help_text="The theme or style for personalization")