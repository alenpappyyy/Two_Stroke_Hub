from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bike
from notifications.utils import notify_user
from dashboard.utils import send_dashboard_update




@receiver(post_save, sender=User)
def create_seller_group(sender, instance, created, **kwargs):
    if created:
        Group.objects.get_or_create(name='Seller')
        
        
        
        

@receiver(post_save, sender=Bike)
def bike_created(sender, instance, created, **kwargs):
    if created:
        notify_user(
            instance.seller,
            f"Your bike '{instance.name}' was listed successfully 🚀"
        )
        
@receiver(post_save, sender=Bike)
def bike_changed(sender, instance, **kwargs):
    send_dashboard_update(instance.seller)