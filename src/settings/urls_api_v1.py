from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("users/", include("apps.users.urls.urls_api_v1")),
    path(
        "docs/",
        include_docs_urls(title="API Documents", authentication_classes=[], permission_classes=[]),
    ),
]
