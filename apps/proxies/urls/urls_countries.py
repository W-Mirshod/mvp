from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.proxies.views.v1.views_countries import CountryViewSet

router = DefaultRouter()
router.register('', CountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
