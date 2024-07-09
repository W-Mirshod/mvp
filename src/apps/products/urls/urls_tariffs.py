from django.urls import path

from .. import views

app_name = "tariffs_api"

urlpatterns = [
    path("", views.GetTariffsView.as_view({"get": "tariff_list"}), name="tariff_list"),
    path("<int:id>/", views.GetTariffsView.as_view({"get": "tariff_by_id"}), name="tariff_by_id"),
]
