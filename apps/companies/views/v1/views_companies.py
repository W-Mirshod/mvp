from rest_framework.permissions import IsAuthenticated

from apps.companies.models.company import Company
from apps.companies.serializers import CompanySerializer, CompanyActivitySerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


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
