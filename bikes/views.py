from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.urls import reverse

from .models import Bike, Category
from .forms import BikeForm

from cart.models import CartItem
from orders.models import Order, OrderItem

from watchlist.models import WatchlistItem
from notifications.utils import notify_user


def bike_list(request):
    bikes = Bike.objects.all()
    categories = Category.objects.all()

    q = request.GET.get("q")
    category = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if q:
        bikes = bikes.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if category:
        bikes = bikes.filter(category__slug=category)

    if min_price:
        bikes = bikes.filter(price__gte=min_price)

    if max_price:
        bikes = bikes.filter(price__lte=max_price)

    return render(request, "bikes/bike_list.html", {
        "bikes": bikes,
        "categories": categories,
    })


def bike_detail(request, pk):
    bike = get_object_or_404(Bike, pk=pk)

    # 🔥 Increase view count
    bike.views += 1
    bike.save(update_fields=["views"])

    # ❤️ Check watchlist
    is_watchlisted = False
    if request.user.is_authenticated:
        is_watchlisted = WatchlistItem.objects.filter(
            watchlist__user=request.user,
            bike=bike
        ).exists()

    return render(request, "bikes/bike_detail.html", {
        "bike": bike,
        "is_watchlisted": is_watchlisted,
    })
def is_seller(user):
    return user.is_authenticated and user.groups.filter(name="Seller").exists()



@login_required
@user_passes_test(is_seller)
def seller_dashboard(request):
    bikes = Bike.objects.filter(seller=request.user).annotate(
        sold_count=Count("orderitem")
    )

    return render(request, "bikes/seller_dashboard.html", {
        "bikes": bikes
    })


@login_required
@user_passes_test(is_seller)
def add_bike(request):
    if request.method == "POST":
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.seller = request.user
            bike.save()
            messages.success(request, "Bike added successfully 🚀")
            return redirect("bikes:seller_dashboard")
    else:
        form = BikeForm()

    return render(request, "bikes/add_bike.html", {"form": form})


@login_required
@user_passes_test(is_seller)
def edit_bike(request, pk):
    bike = get_object_or_404(Bike, pk=pk, seller=request.user)

    if request.method == "POST":
        form = BikeForm(request.POST, request.FILES, instance=bike)
        if form.is_valid():
            form.save()
            return redirect("bikes:seller_dashboard")
    else:
        form = BikeForm(instance=bike)

    return render(request, "bikes/edit_bike.html", {"form": form})


@login_required
@user_passes_test(is_seller)
def delete_bike(request, pk):
    bike = get_object_or_404(Bike, pk=pk, seller=request.user)
    bike.delete()
    messages.success(request, "Bike deleted 🗑️")
    return redirect("bikes:seller_dashboard")


@login_required
def toggle_watchlist(request, pk):
    bike = get_object_or_404(Bike, pk=pk)

    watchlist, _ = Watchlist.objects.get_or_create(user=request.user)

    item = WatchlistItem.objects.filter(
        watchlist=watchlist,
        bike=bike
    ).first()

    if item:
        item.delete()
    else:
        WatchlistItem.objects.create(
            watchlist=watchlist,
            bike=bike
        )

    return redirect("bikes:detail", pk=pk)


@login_required
def watchlist_view(request):
    watchlist = Watchlist.objects.filter(user=request.user).first()
    items = watchlist.items.select_related("bike") if watchlist else []

    return render(request, "bikes/watchlist.html", {
        "items": items
    })


@staff_member_required
def admin_dashboard(request):
    total_bikes = Bike.objects.count()
    total_sellers = Bike.objects.values("seller").distinct().count()

    sold_bikes = Bike.objects.filter(
        orderitem__order__is_paid=True
    ).distinct().count()

    unsold_bikes = Bike.objects.filter(
        orderitem__isnull=True
    ).count()

    top_bikes = (
        OrderItem.objects
        .values("bike__name")
        .annotate(total_sold=Count("id"))
        .order_by("-total_sold")[:5]
    )

    total_revenue = (
        Order.objects
        .filter(is_paid=True)
        .aggregate(total=Sum("amount"))
        .get("total") or 0
    )

    return render(request, "bikes/admin_dashboard.html", {
        "total_bikes": total_bikes,
        "sold_bikes": sold_bikes,
        "unsold_bikes": unsold_bikes,
        "total_sellers": total_sellers,
        "top_bikes": top_bikes,
        "total_revenue": total_revenue,
    })



@staff_member_required
def sales_analytics(request):
    monthly_sales = (
        Order.objects
        .filter(is_paid=True)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    monthly_orders = (
        Order.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    top_bikes = (
        OrderItem.objects
        .values("bike__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    return render(request, "bikes/sales_analytics.html", {
        "monthly_sales": monthly_sales,
        "monthly_orders": monthly_orders,
        "top_bikes": top_bikes,
    })



@login_required
def create_bike(request):
    if request.method == "POST":
        bike = Bike.objects.create(
            seller=request.user,
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
        )

        # 🔔 Send real-time notification
        notify_user(request.user, "Your bike was listed successfully! 🚀")

        return redirect("dashboard:dashboard")

    return render(request, "bikes/create_bike.html")

@login_required
def bike_create(request):
    if request.method == "POST":
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("bikes:bike_list")
    else:
        form = BikeForm()

    return render(request, "bikes/bike_form.html", {"form": form})

@login_required
def compare_view(request):
    compare_ids = request.session.get("compare_bikes", [])
    bikes = Bike.objects.filter(id__in=compare_ids)
    return render(request, "bikes/compare.html", {"bikes": bikes})


@login_required
def toggle_compare(request, bike_id):
    compare = request.session.get("compare_bikes", [])

    if bike_id in compare:
        compare.remove(bike_id)
    else:
        # limit to 3 bikes max
        if len(compare) < 3:
            compare.append(bike_id)

    request.session["compare_bikes"] = compare
    return redirect(request.META.get("HTTP_REFERER", "compare"))



@staff_member_required
def dashboard_view(request):
    total_bikes = Bike.objects.count()

    watchlist_count = WatchlistItem.objects.count()

    most_viewed = Bike.objects.order_by("-views")[:5]

    return render(request, "bikes/dashboard.html", {
        "total_bikes": total_bikes,
        "watchlist_count": watchlist_count,
        "most_viewed": most_viewed,
    })