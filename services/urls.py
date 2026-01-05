from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.services_list, name="services_list"),
    path("home/", views.services_home, name="home"),

    path("book/<int:id>/", views.book_service, name="book_service"),
    path("success/", views.booking_success, name="booking_success"),

    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("cancel/<int:id>/", views.cancel_booking, name="cancel_booking"),

    path("category/<slug:slug>/", views.category_services, name="category_services"),
]
