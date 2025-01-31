import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.proxies.models.proxies import Proxy
from apps.proxies.serializers.file_upload import TextFileUploadSerializer
from apps.proxies.serializers.proxy import ProxySerizalizer
from apps.proxies.tasks import check_proxy_health
from apps.proxies.utils import check_single_proxy
from utils.permissions import IsTokenValid


logger = logging.getLogger(__name__)


class ProxyViewSet(ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerizalizer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, IsTokenValid)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving proxy")
        instance = self.get_object()
        proxy = check_single_proxy(instance)
        serializer = self.get_serializer(proxy)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_proxies(self, request):
        logger.info("Uploading proxies")
        serializer = TextFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            existing_proxies = set()

            for proxy in Proxy.objects.all():
                existing_proxies.add(f"{proxy.host}:{proxy.port}")

            created_proxies = []
            errors = []

            try:
                for line in file:
                    line = line.decode('utf-8').strip()
                    if line:
                        parts = line.split(':')

                        if len(parts) == 2:
                            host, port = parts
                            username = None
                            password = None
                        elif len(parts) == 4:
                            host, port, username, password = parts
                        else:
                            errors.append(f"Invalid proxy format: {line}")
                            continue

                        proxy_key = f"{host}:{port}"

                        if proxy_key in existing_proxies:
                            errors.append(f"Proxy {proxy_key} already exists.")
                        else:
                            Proxy.objects.create(
                                host=host,
                                port=int(port),
                                username=username,
                                password=password
                            )
                            created_proxies.append(proxy_key)

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

    @action(detail=False, methods=['post'], url_path='upload-list')
    def upload_list_proxies(self, request):
        logger.info("Uploading list of proxies")
        proxies = request.data.get('proxies', [])
        existing_proxies = set(f"{proxy.host}:{proxy.port}" for proxy in Proxy.objects.all())
        created_proxies = []
        errors = []

        try:
            for proxy in proxies:
                host = proxy.get('host')
                port = proxy.get('port')
                username = proxy.get('username', None)
                password = proxy.get('password', None)

                if host and port is not None:
                    proxy_key = f"{host}:{port}"

                    if proxy_key in existing_proxies:
                        errors.append(f"Proxy {proxy_key} already exists.")
                    else:
                        Proxy.objects.create(
                            host=host,
                            port=int(port),
                            username=username,
                            password=password
                        )
                        created_proxies.append(proxy_key)

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
