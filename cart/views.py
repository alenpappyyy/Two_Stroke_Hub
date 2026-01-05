from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CartItem, Cart, Watchlist
from parts.models import Part


# 🛒 Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Part, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()
    cart.update_total()

    return redirect("cart_view")


# ➕ Increase quantity
@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user   # 🔐 security
    )

    item.quantity += 1
    item.save()
    item.cart.update_total()

    return redirect("cart_view")


# ➖ Decrease quantity
@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user   # 🔐 security
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    item.cart.update_total()
    return redirect("cart_view")


# 👁️ View cart
@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, "cart/cart.html", {"cart": cart})


# ⭐ Add to watchlist
@login_required
def add_to_watchlist(request, product_id):
    product = get_object_or_404(Part, id=product_id)
    Watchlist.objects.get_or_create(user=request.user, product=product)
    return redirect("watchlist_view")
