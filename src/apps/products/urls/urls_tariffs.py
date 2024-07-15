from django.urls import path

from .. import views

app_name = "tariffs_api"

urlpatterns = [
    path("", views.TariffView.as_view({"get": "list"}), name="tariff_list"),
    path("<int:pk>/", views.TariffView.as_view({"get": "retrieve"}), name="tariff_by_id"),
]
