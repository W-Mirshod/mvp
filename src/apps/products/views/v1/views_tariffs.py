from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from apps.products.models import Tariff
from utils.views import MultiSerializerViewSet


class GetTariffsView(MultiSerializerViewSet):
    queryset = Tariff.objects.none()
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def tariff_list(self, request):
        tariffs = Tariff.objects.all()
        tariffs_list = [
            {
                "id": tariff.id,
                "title": tariff.title,
                "rate": tariff.rate,
                "product": tariff.product.id,
            }
            for tariff in tariffs
        ]
        return Response(tariffs_list, status=status.HTTP_200_OK)

    @transaction.atomic
    def tariff_by_id(self, request, id):
        try:
            tariff = Tariff.objects.get(pk=id)
            tariff_data = {
                "id": tariff.id,
                "title": tariff.title,
                "rate": tariff.rate,
                "product": tariff.product.id,
            }
            return Response(tariff_data, status=status.HTTP_200_OK)
        except Tariff.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
