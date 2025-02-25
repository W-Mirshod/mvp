from rest_framework import serializers

from apps.imap.models import EmailAccount


class FolderSerializer(serializers.Serializer):
    name = serializers.CharField()

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField()
    subject = serializers.CharField()
    from_address = serializers.CharField(source='from')
    date = serializers.CharField()


class EmailAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailAccount
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")