from django.urls import path

from .. import views

app_name = "users_api"

urlpatterns = [
    path(
        "login/",
        views.LoginTokenView.as_view({"post": "login"}),
        name="token_obtain_pair",
    ),
    path("logout/", views.LogoutViewSet.as_view({"post": "logout"}), name="logout"),
    path(
        "registration/",
        views.RegistrationViewSet.as_view({"post": "registration"}),
        name="registration",
    ),
]
