from django.urls import path

from apps.metrics.views import SystemStatusView, MetricsView

urlpatterns = [
    path("status/", SystemStatusView.as_view(), name="system_status"),
    path("metrics/", MetricsView.as_view(), name="metrics"),
]
