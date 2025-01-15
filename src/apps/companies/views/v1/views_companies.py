from rest_framework.permissions import IsAuthenticated

from src.apps.companies.models import Company
from src.apps.companies.serializers import CompanyActivitySerializer, CompanySerializer
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


class CompanyView(MultiSerializerViewSet):
    queryset = Company.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": CompanySerializer,
        "list": CompanySerializer,
        "create": CompanySerializer,
        "destroy": CompanySerializer,
        "update": CompanyActivitySerializer,
    }
