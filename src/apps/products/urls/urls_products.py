from django.urls import path

from src.apps.products.views.v1.views_products import ProductView

app_name = "products_api"

urlpatterns = [
    path("", ProductView.as_view({"get": "list"}), name="product_list"),
    path(
        "<int:pk>/",
        ProductView.as_view({"get": "retrieve"}),
        name="product_by_id",
    ),
]
