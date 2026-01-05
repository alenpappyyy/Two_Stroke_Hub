from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.conf import settings
import razorpay

from bikes.models import Bike
from cart.models import Cart
from .models import Order, OrderItem


class CheckoutView(View):
    def get(self, request, bike_id):
        bike = get_object_or_404(Bike, id=bike_id)
        return render(request, "orders/checkout.html", {"bike": bike})



def create_order(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    order = Order.objects.create(
        user=request.user,
        total_price=bike.price,
        status="PENDING"
    )

    OrderItem.objects.create(
        order=order,
        bike=bike,
        quantity=1,
        price=bike.price
    )

    return redirect("order_success", order_id=order.id)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/success.html", {"order": order})

def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        return redirect("cart_detail")

    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price(),
        is_paid=True  # later connect Razorpay/Stripe
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    cart.items.all().delete()  # 🔥 clear cart after purchase

    return redirect("order_success")
    
@csrf_exempt
def payment_success(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    data = request.POST

    try:
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        client.utility.verify_payment_signature({
            "razorpay_order_id": data.get("razorpay_order_id"),
            "razorpay_payment_id": data.get("razorpay_payment_id"),
            "razorpay_signature": data.get("razorpay_signature"),
        })

        order = Order.objects.get(
            razorpay_order_id=data.get("razorpay_order_id")
        )

        order.razorpay_payment_id = data.get("razorpay_payment_id")
        order.razorpay_signature = data.get("razorpay_signature")
        order.is_paid = True
        order.status = "PAID"
        order.save()

        return render(request, "orders/success.html", {"order": order})

    except Exception:
        return HttpResponseBadRequest()
