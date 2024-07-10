from django.urls import path

from .. import views

app_name = "users_api"

urlpatterns = [
    path(
        "<int:pk>/",
        views.UserViewSet.as_view({"get": "retrieve"}),
        name="manage",
    ),
    path(
        "email_verify/",
        views.EmailVerificationView.as_view({"post": "email_verify"}),
        name="email_verify",
    ),
    path("login/", views.LoginTokenView.as_view({"post": "login"}), name="token_obtain_pair"),
    path("logout/", views.BlacklistTokenView.as_view({"post": "logout"}), name="logout"),
    path(
        "registration/",
        views.RegistrationViewSet.as_view({"post": "registration"}),
        name="registration",
    ),
]
