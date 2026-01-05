from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from bikes.models import Bike
from .models import WatchlistItem

@login_required
def watchlist_view(request):
    items = WatchlistItem.objects.filter(user=request.user)
    return render(request, "watchlist/watchlist.html", {"items": items})


@login_required
def add_to_watchlist(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    WatchlistItem.objects.get_or_create(user=request.user, bike=bike)
    return redirect("watchlist:watchlist")


@login_required
def remove_from_watchlist(request, bike_id):
    WatchlistItem.objects.filter(
        user=request.user,
        bike_id=bike_id
    ).delete()
    return redirect("watchlist:watchlist")
