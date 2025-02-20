import logging
import os

from apps.mail_servers.export_service import ExportService
from apps.mail_servers.file_service import FileService
from apps.mail_servers.security import SecurityUtils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class FileUploadView(APIView):
    """File upload with materials"""

    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["files"],
        operation_summary="Upload file",
        operation_description="Uploading a file with materials (databases, SMTP, proxy)",
        manual_parameters=[
            openapi.Parameter(
                "file",
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Upload file",
            ),
            openapi.Parameter(
                "session",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Session ID",
            ),
            openapi.Parameter(
                "type",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                enum=["base", "smtp", "proxy"],
                description="Materials type",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success file processed",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "processed": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "failed": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            ),
            400: openapi.Response(
                description="Parameters error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def post(self, request):
        file_obj = request.FILES.get("file")
        session = request.POST.get("session")

        try:
            # File validation
            SecurityUtils.validate_file_upload(file_obj)

            # Read file content directly
            content = file_obj.read().decode("utf-8")

            processor = FileService.get_processor(request.POST.get("type"))
            result = processor(content, session)

            return Response(result)

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExportView(APIView):
    """Data export"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["export"],
        operation_summary="Export data",
        operation_description="Exporting data to CSV format",
        manual_parameters=[
            openapi.Parameter(
                "type",
                openapi.IN_PATH,
                description="Data type (bases/smtp/proxy/logs)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "session",
                openapi.IN_PATH,
                description="Session name",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="CSV file",
                schema=openapi.Schema(type=openapi.TYPE_STRING, format="binary"),
            ),
            400: openapi.Response(description="Parameters error"),
        },
    )
    def get(self, request, type, session):
        try:
            export_map = {
                "bases": ExportService.export_bases,
                "smtp": ExportService.export_smtp,
                "proxy": ExportService.export_proxy,
                "logs": ExportService.export_logs,
            }

            exporter = export_map.get(type)
            if not exporter:
                return Response(
                    {"error": f"Invalid export type: {type}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            content = exporter(session)
            response = HttpResponse(content, content_type="text/csv")
            response["Content-Disposition"] = (
                f'attachment; filename="{type}_{session}.csv"'
            )
            return response

        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
