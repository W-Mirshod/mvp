from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.smtp_checker.views.v1.smtp_views import (
    ServerCheckerSettingsAPIView,
    ServerCheckerTaskAPIView,
    ServerCheckerTaskResultAPIView,
    SMTPStatisticsAPIView,
)

app_name = "server_checker"

router = DefaultRouter()
router.register(
    r"settings", ServerCheckerSettingsAPIView, basename="server_checker_settings"
)
router.register(r"tasks", ServerCheckerTaskAPIView, basename="server_checker_tasks")
router.register(
    r"results", ServerCheckerTaskResultAPIView, basename="server_checker_results"
)

urlpatterns = [
    path("", include(router.urls)),
    path("statistics/", SMTPStatisticsAPIView.as_view(), name="smtp_statistics"),
]
