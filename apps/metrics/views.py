from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from django.db import connection
import redis

from apps.metrics.constants import MonitoringConstants
from celery_scripts.celery_app import celery_app
from config.settings import REDIS_URL
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants


logger = logging.getLogger("app")


class SystemStatusView(APIView):
    """API endpoint for system monitoring"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["monitoring"],
        operation_summary="Monitoring status",
        operation_description="Check database, Redis, and Celery connectivity.\nValidate individual component status.\nReturn overall system health with component details.",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "components": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "database": openapi.Schema(type=openapi.TYPE_STRING),
                                "redis": openapi.Schema(type=openapi.TYPE_STRING),
                                "celery": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            503: openapi.Response(
                description="Serves error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def get(self, request):
        components = {}

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            components["database"] = MonitoringConstants.CONNECTED_SYSTEM_STATUS
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SystemStatusView.get() database: Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Database connection failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Database connection failed:{ex=}")
            components["database"] = MonitoringConstants.DISCONNECTED_SYSTEM_STATUS

        try:
            redis_client = redis.StrictRedis.from_url(REDIS_URL)
            redis_client.ping()
            components["redis"] = MonitoringConstants.CONNECTED_SYSTEM_STATUS
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SystemStatusView.get() redis: Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Redis connection failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Redis connection failed: {ex=}")
            components["redis"] = MonitoringConstants.DISCONNECTED_SYSTEM_STATUS

        try:
            celery_inspect = celery_app.control.inspect()
            if celery_inspect and celery_inspect.ping():
                components["celery"] = MonitoringConstants.CONNECTED_SYSTEM_STATUS
            else:
                components["celery"] = MonitoringConstants.DISCONNECTED_SYSTEM_STATUS
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SystemStatusView.get() celery: Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Celery status check failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Celery status check failed: {ex=}")
            components["celery"] = MonitoringConstants.DISCONNECTED_SYSTEM_STATUS

        if all(
            status == MonitoringConstants.CONNECTED_SYSTEM_STATUS
            for status in components.values()
        ):
            overall_status = MonitoringConstants.HEALTHY_OVERALL_SYSTEM_STATUS
        else:
            overall_status = MonitoringConstants.UNHEALTHY_OVERALL_SYSTEM_STATUS

        status_info = {
            "status": overall_status,
            "components": components,
        }

        return Response(
            status_info,
            status=(
                200
                if overall_status == MonitoringConstants.HEALTHY_OVERALL_SYSTEM_STATUS
                else 503
            ),
        )


class MetricsView(APIView):
    """API endpoint for getting Prometheus metrics"""

    permission_classes = []

    @swagger_auto_schema(
        tags=["monitoring"],
        operation_summary="Prometheus metrics",
        operation_description="Retrieve Prometheus formatted metrics.\nGenerate latest metrics snapshot from the server.\nReturn metrics as a binary HTTP response.",
        responses={
            200: openapi.Response(
                description="Success metrics in Prometheus format",
                schema=openapi.Schema(type=openapi.TYPE_STRING, format="binary"),
            )
        },
    )
    def get(self, request):
        metrics_page = generate_latest()
        return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)
