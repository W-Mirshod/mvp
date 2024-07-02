import time

from django.middleware.common import MiddlewareMixin
from django.db import reset_queries, connection
from django.conf import settings


class DebugQuerysetsWare(MiddlewareMixin):
    EXCLUDE_URL = [
        "/admin/jsi18n/",
    ]

    def process_request(self, request):
        if settings.SQL_DEBUG:
            reset_queries()
            self.run_time = time.time()

    def process_response(self, request, response):
        if settings.SQL_DEBUG:
            url = request.path
            if url in self.EXCLUDE_URL:
                return response

            times = round(sum([float(x.get("time")) for x in connection.queries]), 3)

            strs = [
                f"sql_count: {len(connection.queries)}",
                f"sql_time: {times}",
                f"url: {url}",
            ]
            if hasattr(self, "run_time"):
                strs.append(f"run_time: {round(time.time() - self.run_time, 3)}")
            view = getattr(response, "renderer_context", {}).get("view")
            if view:
                strs.append(f"{view.__module__}.{view.__class__.__name__}")
            strs.append(request.method)
            print(" | ".join(strs))
        return response
