from django.shortcuts import render
from bikes.models import Bike
from django.db.models import Q

def home(request):
    query = request.GET.get("q")

    bikes = Bike.objects.all()

    if query:
        bikes = bikes.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    context = {
        "featured_bikes": bikes,
        "query": query,
        "is_seller": (
            request.user.is_authenticated and
            request.user.groups.filter(name="Seller").exists()
        )
    }

    return render(request, "home.html", context)
