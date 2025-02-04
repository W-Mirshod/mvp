from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet

app_name = 'imap'

router = DefaultRouter()
router.register(r'emails', EmailViewSet, basename='email')

urlpatterns = router.urls

urlpatterns += [
    path('emails/check/', EmailViewSet.as_view({'get': 'check'}), name='email-check'),
    path('emails/latest/', EmailViewSet.as_view({'get': 'latest'}), name='email-latest'),
    path('emails/stats/', EmailViewSet.as_view({'get': 'stats'}), name='email-stats'),
]
