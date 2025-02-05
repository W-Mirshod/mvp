from rest_framework import serializers
from apps.smtp_checker.models.models import SMTPCheckerSettings, SMTPCheckerTask, SMTPCheckerTaskResult


class SMTPCheckerSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPCheckerSettings
        fields = "__all__"
        read_only_fields = ("id", "user")


class SMTPCheckerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPCheckerTask
        fields = "__all__"
        read_only_fields = ("id", "status", "user")


class SMTPCheckerTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPCheckerTaskResult
        fields = "__all__"
        read_only_fields = ("id", "task", "server")
