import threading

# Create local storage for each thread
_request_local = threading.local()


def get_current_user():
    return getattr(_request_local, "user", None)


def get_current_url():
    return getattr(_request_local, "url", None)


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.user = getattr(request, "user", None)
        _request_local.url = request.build_absolute_uri()
        response = self.get_response(request)
        del _request_local.user
        del _request_local.url
        return response
