from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from .utils import seller_required
from .forms import BikeForm, PartForm

from bikes.models import Bike
from parts.models import Part
from orders.models import Order
from watchlist.models import WatchlistItem
from profiles.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page




class DashboardPasswordChangeView(PasswordChangeView):
    template_name = "dashboard/change_password.html"
    success_url = reverse_lazy("dashboard:profile")


@login_required
@cache_page(60 * 2)  
def dashboard(request):
    user = request.user

    my_bikes = Bike.objects.filter(seller=user)

    monthly_data = (
        my_bikes
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    months = [d["month"].strftime("%b") for d in monthly_data if d["month"]]
    totals = [d["total"] for d in monthly_data]

    notifications = request.user.notifications.filter(is_read=False)[:5]

    context = {
        # 📊 Stats
        "total_bikes": my_bikes.count(),
        "active_bikes": my_bikes.filter(is_sold=False).count(),
        "sold_bikes": my_bikes.filter(is_sold=True).count(),
        "total_views": my_bikes.aggregate(total=Sum("views"))["total"] or 0,
        "watchlisted_count": WatchlistItem.objects.filter(bike__in=my_bikes).count(),

        # 🏍 Recent
        "recent_bikes": my_bikes.order_by("-created_at")[:5],

        # 📈 Chart
        "chart_labels": months,
        "chart_data": totals,

        # 🔔 Notifications
        "notifications": notifications,
        "notifications_count": notifications.count(),
    }

    return render(request, "dashboard/dashboard.html", context)




@login_required
def profile(request):
    return render(request, "dashboard/profile.html")


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("dashboard:profile")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, "dashboard/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })



@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "dashboard/orders.html", {
        "orders": orders,
        "total_orders": orders.count(),
        "pending_orders": orders.filter(status="pending").count(),
        "delivered_orders": orders.filter(status="delivered").count(),
        "revenue": orders.aggregate(total=Sum("total_price"))["total"] or 0,
    })


def my_listings(request):
    bikes = Bike.objects.filter(seller=request.user)

    watchlisted_count = WatchlistItem.objects.filter(
        bike__in=bikes
    ).count()

    return render(request, "dashboard/dashboard.html", {
        "bikes": bikes,
        "watchlisted_count": watchlisted_count,
    })


@login_required
def watchlist(request):
    items = (
        WatchlistItem.objects
        .filter(user=request.user)
        .select_related("bike")
    )
    return render(request, "dashboard/watchlist.html", {"items": items})


@login_required
def dashboard_logout(request):
    logout(request)
    return redirect("login")


@login_required
@seller_required
def seller_dashboard(request):
    from orders.models import OrderItem

    seller_bikes = Bike.objects.filter(seller=request.user)
    seller_parts = Part.objects.filter(seller=request.user)

    earnings = (
        OrderItem.objects
        .filter(seller=request.user)
        .aggregate(total=Sum("total_price"))["total"] or 0
    )

    context = {
        "bikes_count": seller_bikes.count(),
        "parts_count": seller_parts.count(),
        "earnings": earnings,
        "recent_bikes": seller_bikes.order_by("-created_at")[:5],
    }

    return render(request, "dashboard/seller/dashboard.html", context)


@login_required
def seller_products(request):
    return render(request, "dashboard/seller/products.html")


@login_required
def seller_orders(request):
    return render(request, "dashboard/seller/orders.html")


@login_required
def seller_earnings(request):
    return render(request, "dashboard/seller/earnings.html")


@login_required
def seller_profile(request):
    return render(request, "dashboard/seller/profile.html")


@login_required
def seller_product_create(request, product_type):
    return render(
        request,
        "dashboard/seller/product_form.html",
        {"product_type": product_type}
    )


@login_required
def seller_product_edit(request, product_type, pk):
    return render(
        request,
        "dashboard/seller/product_form.html",
        {
            "product_type": product_type,
            "pk": pk,
            "edit": True,
        }
    )


@login_required
def seller_product_delete(request, product_type, pk):
    return redirect("dashboard:seller_products")


@login_required
def favorites(request):
    return render(request, "dashboard/favorites.html")


@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")


@login_required
def buyer_dashboard(request):
    return render(request, "dashboard/roles/buyer_dashboard.html")


@login_required
def mechanic_dashboard(request):
    return render(request, "dashboard/roles/mechanic_dashboard.html")


@login_required
def admin_dashboard(request):
    return render(request, "dashboard/roles/admin_dashboard.html")


@login_required
def stub(request):
    return render(request, "dashboard/coming_soon.html")
