from django.urls import path

from .. import views


app_name = "users_api"

urlpatterns = [
    path("login/", views.LoginTokenView.as_view({"post": "login"}), name="token_obtain_pair"),
    path("api/1.0/token_refresh/", views.RefreshTokenView.as_view({"post": "refresh"}), name="token_refresh"),
    path(
        "registration/",
        views.RegistrationViewSet.as_view({"post": "registration"}),
        name="registration",
    ),
]
