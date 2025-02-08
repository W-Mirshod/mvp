from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.proxies.models import ProxyConfig
from apps.proxies.serializers.proxy_config import ProxyConfigSerializer
from utils.permissions import IsTokenValid, IsOwner


class ProxyConfigViewSet(viewsets.ModelViewSet):
    queryset = ProxyConfig.objects.none()
    serializer_class = ProxyConfigSerializer
    permission_classes = (IsAuthenticated, IsTokenValid, IsOwner)

    def get_queryset(self):
        return ProxyConfig.objects.filter(author_id=self.request.user.pk)
