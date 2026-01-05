from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # Main dashboard
    path("", views.dashboard, name="dashboard"),

    # Profile
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # User features
    path("my-listings/", views.my_listings, name="my_listings"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("favorites/", views.favorites, name="favorites"),
    path("orders/", views.orders, name="orders"),
    path("settings/", views.settings_view, name="settings"),

    # Auth
    path("logout/", views.dashboard_logout, name="logout"),

    # Role dashboards
    path("buyer/", views.buyer_dashboard, name="buyer_dashboard"),
    path("mechanic/", views.mechanic_dashboard, name="mechanic_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),

    # Seller dashboard
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/products/", views.seller_products, name="seller_products"),
    path("seller/orders/", views.seller_orders, name="seller_orders"),
    path("seller/earnings/", views.seller_earnings, name="seller_earnings"),
    path("seller/profile/", views.seller_profile, name="seller_profile"),

    # Seller product CRUD
    path(
        "seller/product/add/<str:product_type>/",
        views.seller_product_create,
        name="seller_product_add"
    ),
    path(
        "seller/product/<str:product_type>/edit/<int:pk>/",
        views.seller_product_edit,
        name="seller_product_edit"
    ),
    path(
        "seller/product/<str:product_type>/delete/<int:pk>/",
        views.seller_product_delete, name="seller_product_delete"),


    path("watchlist/", views.watchlist, name="watchlist"),
    
    path("password/change/", views.DashboardPasswordChangeView.as_view(), name="change_password"),

]
