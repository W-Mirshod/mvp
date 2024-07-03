from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_url

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/1.0/", include("settings.urls_api_v1")),
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
