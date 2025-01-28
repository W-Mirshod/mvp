from django.urls import path

from apps.email_analysis.views.v1.views_email_analysis import (
    SpamDetectionView,
)

app_name = "email_analysis_api"

urlpatterns = [
    path(
        "spam_detection/",
        SpamDetectionView.as_view(),
        name='spam_detection'
    ),
]
