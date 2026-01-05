from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bike(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Part(models.Model):
    bike = models.ForeignKey("marketplace.Bike", on_delete=models.CASCADE, related_name="parts")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey("marketplace.Bike", on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_type} - {self.bike}"


# 🆕 NEW BLOG POST MODEL
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blogs/")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 🆕 NEW OWNERS GROUP POSTS MODEL
class OwnersGroupPost(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
