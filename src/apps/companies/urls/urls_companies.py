from django.urls import path

from .. import views

app_name = "companies_api"

urlpatterns = [
    path("", views.CompanyView.as_view({"get": "list"}), name="company_list"),
    path(
        "<int:pk>/",
        views.CompanyView.as_view({"get": "retrieve", "post": "create", "delete": "destroy"}),
        name="company_by_id",
    ),
    path(
        "activity/<int:pk>", views.CompanyView.as_view({"patch": "update"}), name="company_activity"
    ),
]
