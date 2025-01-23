from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.proxies.models.proxies import Proxy
from apps.proxies.serializers.proxy import ProxySerizalizer
from utils.permissions import IsTokenValid


class ProxyViewSet(ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerizalizer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, IsTokenValid)
