from django.urls import path
from .views import (
    cart_view,
    add_to_cart,
    increase_quantity,
    decrease_quantity,
    add_to_watchlist
)

app_name = "cart"

urlpatterns = [
    path("", cart_view, name="cart_view"),

    # Add products to cart
    path("add/<str:product_type>/<int:product_id>/", add_to_cart, name="add_to_cart"),

    # Modify quantity
    path("increase/<int:item_id>/", increase_quantity, name="increase_quantity"),
    path("decrease/<int:item_id>/", decrease_quantity, name="decrease_quantity"),

    # Watchlist
    path("watchlist/add/<int:product_id>/", add_to_watchlist, name="add_to_watchlist"),
]
