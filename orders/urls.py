from django.urls import path
from .views import CheckoutView, create_order, order_success
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/<int:bike_id>/", CheckoutView.as_view(), name="checkout"),
    path("create/<int:bike_id>/", create_order, name="create_order"),
    path("success/<int:order_id>/", order_success, name="order_success"),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
]
