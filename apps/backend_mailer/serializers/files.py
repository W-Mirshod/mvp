from apps.backend_mailer.models.files import UploadedFile
from rest_framework import serializers

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at']
