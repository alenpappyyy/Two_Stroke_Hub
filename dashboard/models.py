from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shop_cart'  # ✅ UNIQUE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_cart'  # ✅ DIFFERENT
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_orders'  # ✅ UNIQUE
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
