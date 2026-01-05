from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_BUYER = "buyer"
    ROLE_SELLER = "seller"
    ROLE_MECHANIC = "mechanic"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_BUYER, "Buyer"),
        (ROLE_SELLER, "Seller"),
        (ROLE_MECHANIC, "Mechanic"),
        (ROLE_ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_BUYER)

    def __str__(self):
        return f"{self.username} ({self.role})"
