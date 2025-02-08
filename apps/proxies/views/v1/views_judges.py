from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.proxies.models import Judge
from apps.proxies.serializers.judge import JudgeSerializer
from utils.permissions import IsTokenValid


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    permission_classes = (IsAuthenticated, IsTokenValid)
