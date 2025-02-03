from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.proxies.models import Country
from apps.proxies.serializers.country import CountrySerializer
from utils.permissions import IsTokenValid


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticated, IsTokenValid)
