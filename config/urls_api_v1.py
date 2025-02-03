from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("users/", include("apps.users.urls.urls_api_v1")),
    path("servers/", include("apps.mail_servers.urls.urls_servers")),
    path("products/", include("apps.products.urls.urls_products")),
    path("tariffs/", include("apps.products.urls.urls_tariffs")),
    path("messages/", include("apps.backend_mailer.urls.message_v1")),
    path("campaign/", include("apps.mailers.urls.campaign_v1")),
    path("companies/", include("apps.companies.urls.urls_companies")),
    path("monitoring/", include("apps.metrics.urls")),
    path("proxies/", include("apps.proxies.urls.urls_proxies")),
    path("judges/", include("apps.proxies.urls.urls_judges")),
    path("countries/", include("apps.proxies.urls.urls_countries")),
    path("configs/", include("apps.proxies.urls.urls_configs")),
    path("email-analysis/", include("apps.email_analysis.urls.urls_email_analysis")),
    path(
        "docs/",
        include_docs_urls(
            title="API Documents", authentication_classes=[], permission_classes=[]
        ),
    ),
]
