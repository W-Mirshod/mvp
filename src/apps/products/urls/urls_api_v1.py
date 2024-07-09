from django.urls import path

from .. import views

app_name = "products_api"

urlpatterns = [
    path("", views.GetProductsView.as_view({"get": "product_list"}), name="product_list"),
    path(
        "<int:id>/", views.GetProductsView.as_view({"get": "product_by_id"}), name="product_by_id"
    ),
]
