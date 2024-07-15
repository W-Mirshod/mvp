from django.urls import path

from .. import views

app_name = "products_api"

urlpatterns = [
    path("", views.ProductView.as_view({"get": "list"}), name="product_list"),
    path("<int:pk>/", views.ProductView.as_view({"get": "retrieve"}), name="product_by_id"),
]
