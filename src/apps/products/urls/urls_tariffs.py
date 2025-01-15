from django.urls import path

from src.apps.products.views.v1.views_tariffs import TariffView

app_name = "tariffs_api"

urlpatterns = [
    path("", TariffView.as_view({"get": "list"}), name="tariff_list"),
    path("<int:pk>/", TariffView.as_view({"get": "retrieve"}), name="tariff_by_id"),
]
