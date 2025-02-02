from rest_framework import serializers

from apps.proxies.models import Judge


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = ['id', 'url']
        