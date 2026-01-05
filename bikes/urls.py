from django.urls import path
from . import views

app_name = 'bikes'

urlpatterns = [
    # Public
    path('', views.bike_list, name='bike_list'),
    path("", views.bike_list, name="bikes_store"),  
    path('<int:pk>/', views.bike_detail, name='detail'),

    # Seller
    path('add/', views.add_bike, name='add_bike'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('edit/<int:pk>/', views.edit_bike, name='edit_bike'),
    path('delete/<int:pk>/', views.delete_bike, name='delete_bike'),

    # Watchlist
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/toggle/<int:pk>/', views.toggle_watchlist, name='toggle_watchlist'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("compare/", views.compare_view, name="compare"),
    path("compare/toggle/<int:bike_id>/", views.toggle_compare, name="toggle_compare"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("create/", views.bike_create, name="bike_create"),

]
