import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.proxies.models.proxies import Proxy
from apps.proxies.serializers.file_upload import TextFileUploadSerializer
from apps.proxies.serializers.proxy import ProxySerizalizer
from apps.proxies.tasks import check_proxy_health
from apps.proxies.utils import check_single_proxy, get_existing_proxies, validate_and_create_proxy, process_proxies
from utils.permissions import IsTokenValid


logger = logging.getLogger(__name__)


class ProxyViewSet(ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerizalizer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, IsTokenValid)

    @swagger_auto_schema(
        operation_summary="Retrieve proxy details",
        operation_description="Fetch details of a specific proxy.\nCheck the proxy health.\nReturn detailed serialized data."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving proxy")
        instance = self.get_object()
        proxy = check_single_proxy(instance)
        serializer = self.get_serializer(proxy)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Upload proxies from a text file",
        operation_description="Upload proxies from a text file.\nValidate proxy format and create new proxies.\nReturn upload status and error messages.",
        request_body=TextFileUploadSerializer,
    )
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_proxies(self, request):
        logger.info("Uploading proxies")
        serializer = TextFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            existing_proxies = get_existing_proxies()
            created_proxies = []
            errors = []

            try:
                for line in file:
                    line = line.decode('utf-8').strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) in (2, 4):
                            host, port = parts[:2]
                            username = parts[2] if len(parts) == 4 else None
                            password = parts[3] if len(parts) == 4 else None
                            proxy_key, error = validate_and_create_proxy(host, port, username, password,
                                                                               existing_proxies)
                            if proxy_key:
                                created_proxies.append(proxy_key)
                            if error:
                                errors.append(error)
                        else:
                            errors.append(f"Invalid proxy format: {line}")

                check_proxy_health.delay()

                response_data = {
                    "message": "Proxies uploaded successfully!",
                    "created": created_proxies,
                    "errors": errors
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error uploading proxies: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Upload a list of proxies",
        operation_description="Upload a list of proxies.\nValidate proxy format and create new proxies.\nReturn upload status and error messages.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'proxies': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Proxy string in the format host:port or host:port:username:password"
                    ),
                    description="List of proxy strings"
                )
            }
        )
    )
    @action(detail=False, methods=['post'], url_path='upload-list')
    def upload_list_proxies(self, request):
        logger.info("Uploading list of proxies")
        proxies = request.data.get('proxies', [])
        existing_proxies = get_existing_proxies()

        created_proxies, errors = process_proxies(proxies, existing_proxies)

        try:
            check_proxy_health.delay()

            response_data = {
                "message": "Proxies uploaded successfully!",
                "created": created_proxies,
                "errors": errors
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error uploading list of proxies: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
