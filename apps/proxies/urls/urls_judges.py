from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.proxies.views.v1.views_judges import JudgeViewSet

router = DefaultRouter()
router.register('', JudgeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
