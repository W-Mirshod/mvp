from django.contrib import admin
from django.urls import include, path
from config.yasg import urlpatterns as doc_url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/1.0/", include("config.urls_api_v1")),
        path("prometheus/", include("django_prometheus.urls")),
        path(r"ht/", include("health_check.urls")),
        path("silk/", include("silk.urls", namespace="silk")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + doc_url
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    ]
