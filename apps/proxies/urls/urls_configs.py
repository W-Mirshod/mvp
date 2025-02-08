from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.proxies.views.v1.views_proxy_configs import ProxyConfigViewSet

router = DefaultRouter()
router.register("", ProxyConfigViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
