from django.urls import path, include
from rest_framework import routers

from apps.notify.views.v1.notify_views import (
    NotificationViewSet,
)

router = routers.DefaultRouter()

router.register("notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
