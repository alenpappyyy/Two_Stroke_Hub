from django.conf import settings
from django.db import models
from bikes.models import Bike


class WatchlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist_items"
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name="watchlisted_items" 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "bike")

    def __str__(self):
        return f"{self.user} → {self.bike}"
