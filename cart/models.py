from django.db import models
from django.contrib.auth import get_user_model
from parts.models import Part  # Only Part is used in cart

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"{self.user}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)


    def total_price(self):
        return self.product.price * self.quantity
    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Watchlist(models.Model):
    """
    This watchlist is for PARTS only.
    (Bike watchlist is inside the bikes app)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='part_watchlist'
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='watchlisted_by'
    )

    def __str__(self):
        return f"{self.user} → {self.part}"
