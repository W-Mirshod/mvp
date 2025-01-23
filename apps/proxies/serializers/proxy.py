from rest_framework.serializers import ModelSerializer

from ..models.proxies import Proxy


class ProxySerizalizer(ModelSerializer):
    class Meta:
        model = Proxy
        fields = '__all__'
        read_only_fields = ('id', 'is_active', 'country', 'country_code', 'anonymity', 'timeout', 'last_time_checked')
