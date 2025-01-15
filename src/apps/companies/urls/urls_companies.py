from django.urls import path

from src.apps.companies.views.v1.views_companies import CompanyView

app_name = "companies_api"

urlpatterns = [
    path("", CompanyView.as_view({"get": "list"}), name="company_list"),
    path(
        "<int:pk>/",
        CompanyView.as_view(
            {"get": "retrieve", "post": "create", "delete": "destroy"}
        ),
        name="company_by_id",
    ),
    path(
        "activity/<int:pk>",
        CompanyView.as_view({"patch": "update"}),
        name="company_activity",
    ),
]
