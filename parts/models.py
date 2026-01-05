from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Part(models.Model):

    CATEGORY_CHOICES = [
        ('engine', 'Engine'),
        ('exhaust', 'Exhaust'),
        ('suspension', 'Suspension'),
        ('brakes', 'Brakes'),
        ('body', 'Body'),
    ]

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='parts',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    category = models.CharField(
        max_length=120,
        choices=CATEGORY_CHOICES,
        db_index=True
    )

    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to='parts/',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name
