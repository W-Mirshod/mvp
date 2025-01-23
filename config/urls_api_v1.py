from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("users/", include("apps.users.urls.urls_api_v1")),
    path("servers/", include("apps.mail_servers.urls.urls_servers")),
    path("products/", include("apps.products.urls.urls_products")),
    path("tariffs/", include("apps.products.urls.urls_tariffs")),
    path("messages/", include("apps.mailers.urls.message")),
    path("companies/", include("apps.companies.urls.urls_companies")),
    path("monitoring/", include("apps.metrics.urls")),
    path("proxies/", include("apps.proxies.urls.urls_proxies")),
    path(
        "docs/",
        include_docs_urls(
            title="API Documents", authentication_classes=[], permission_classes=[]
        ),
    ),
]
