from django.urls import path

from .. import views

app_name = "users_api"

urlpatterns = [
    path("login/", views.LoginTokenView.as_view({"post": "login"}), name="token_obtain_pair"),
]
