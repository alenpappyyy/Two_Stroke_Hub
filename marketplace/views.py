from django.shortcuts import render
from .models import Bike, BlogPost, OwnersGroupPost

def home(request):
    featured_bikes = Bike.objects.filter(is_featured=True).order_by("position")[:4]
    left_sidebar_bikes = Bike.objects.filter(category="sidebar_left")[:2]
    right_sidebar_bikes = Bike.objects.filter(category="sidebar_right")[:1]

    megamart_bikes = Bike.objects.filter(category="megamart")[:3]
    msamart_bikes = Bike.objects.filter(category="msamart")[:3]

    blog = BlogPost.objects.order_by("-created_at").first()
    owners_posts = OwnersGroupPost.objects.order_by("-created_at")[:5]

    return render(request, "marketplace/home.html", {
        "featured_bikes": featured_bikes,
        "left_sidebar_bikes": left_sidebar_bikes,
        "right_sidebar_bikes": right_sidebar_bikes,
        "megamart_bikes": megamart_bikes,
        "msamart_bikes": msamart_bikes,
        "blog": blog,
        "owners_posts": owners_posts,
    })



def marketplace_home(request):
    return render(request, "marketplace/home.html")


def bikes_store(request):
    return render(request, "bikes/bikes_store.html")
