class Singleton(object):

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class LoggedInUser(Singleton):
    """Singleton to store the user,
    on whose behalf the request is being made
    """

    __metaclass__ = Singleton

    request = None
    user = None
    address = None

    def set_data(self, request):
        self.request = id(request)
        if request.user.is_authenticated:
            self.user = request.user
            self.address = request.META.get("REMOTE_ADDR")

    @property
    def current_user(self):
        return self.user

    @property
    def have_user(self):
        return self.user is not None


class LoggedInUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Init LoggedInUser
        """
        logged_in_user = LoggedInUser()
        logged_in_user.set_data(request)

        response = self.get_response(request)

        return response
