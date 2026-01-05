from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

User = get_user_model()


# -----------------------------
# Category Model
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name




class Bike(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='bikes/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bikes'
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bikes")
    is_sold = models.BooleanField(default=False)  # ✅ ADD THIS

    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)  # ✅ ADD THIS

    def __str__(self):
        return self.name





class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='active')
    image = models.ImageField(upload_to='bikes/', blank=True, null=True)

    def __str__(self):
        return self.title



@login_required
def toggle_watchlist(request, pk):
    bike = get_object_or_404(Bike, pk=pk)

    item = WatchlistItem.objects.filter(
        user=request.user,
        bike=bike
    ).first()

    if item:
        item.delete()
    else:
        WatchlistItem.objects.create(
            user=request.user,
            bike=bike
        )

    return redirect("bikes:detail", pk=pk)