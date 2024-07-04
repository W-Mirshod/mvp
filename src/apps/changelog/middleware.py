import threading

_request_local = threading.local()

def get_current_user():
    return getattr(_request_local, 'user', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.user = getattr(request, 'user', None)
        response = self.get_response(request)
        return response
