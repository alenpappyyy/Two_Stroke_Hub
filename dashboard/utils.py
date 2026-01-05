# dashboard/utils.py
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages
from bikes.models import Bike
from watchlist.models import WatchlistItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        # allow staff/admin too
        if getattr(request.user, 'role', None) == 'seller' or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You must be a seller to access that page.")
        return redirect('dashboard:dashboard')
    return _wrapped


def send_dashboard_update(user):
    bikes = Bike.objects.filter(seller=user)

    data = {
        "total_bikes": bikes.count(),
        "active_bikes": bikes.filter(is_sold=False).count(),
        "sold_bikes": bikes.filter(is_sold=True).count(),
        "total_views": bikes.aggregate(total=Sum("views"))["total"] or 0,
        "watchlisted_count": WatchlistItem.objects.filter(bike__in=bikes).count(),
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"dashboard_{user.id}",
        {
            "type": "dashboard_update",
            "data": data,
        }
    )