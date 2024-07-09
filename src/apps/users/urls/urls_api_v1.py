from django.urls import path

from ..views import LoginTokenView, RefreshTokenView, RegistrationViewSet

app_name = "users_api"

urlpatterns = [
    path("login/", LoginTokenView.as_view({"post": "login"}), name="token_obtain_pair"),
    path(
        "token_refresh/",
        RefreshTokenView.as_view({"post": "refresh"}),
        name="token_refresh",
    ),
    path(
        "registration/",
        RegistrationViewSet.as_view({"post": "registration"}),
        name="registration",
    ),
]
