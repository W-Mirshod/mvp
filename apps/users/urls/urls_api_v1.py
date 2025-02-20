from django.urls import path

from apps.users.views.v1.views_users import (
    UserViewSet,
    EmailVerificationView,
    LoginTokenView,
    BlacklistTokenView,
    RefreshTokenView,
    RegistrationViewSet,
    OneTimeJWTFunctionsViewSet,
)

app_name = "users_api"


urlpatterns = [
    path(
        "<int:pk>/",
        UserViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
        name="manage",
    ),
    path(
        "email_verify/",
        EmailVerificationView.as_view({"get": "email_verify"}),
        name="email_verify",
    ),
    path(
        "login/",
        LoginTokenView.as_view({"post": "login"}),
        name="token_obtain_pair",
    ),
    path("logout/", BlacklistTokenView.as_view({"post": "logout"}), name="logout"),
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
    path(
        "get_one_time_jwt/",
        RegistrationViewSet.as_view({"post": "get_one_time_jwt"}),
        name="get_one_time_jwt",
    ),
    path(
        "restore_password/",
        OneTimeJWTFunctionsViewSet.as_view({"patch": "restore_password"}),
        name="restore_password",
    ),
]
