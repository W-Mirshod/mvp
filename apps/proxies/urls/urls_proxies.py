from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.proxies.views.v1.views_proxies import ProxyViewSet

router = DefaultRouter()
router.register("", ProxyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
