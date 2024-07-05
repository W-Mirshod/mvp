from django.urls import path

from .. import views

app_name = "users_api"

urlpatterns = [
    path("login/", views.LoginTokenView.as_view({"post": "login"}), name="token_obtain_pair"),
    path(
        "email_verify/",
        views.EmailVerificationView.as_view({"post": "email_verify"}),
        name="email_verify",
    ),
]
