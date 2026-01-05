from django.urls import path
from . import views

app_name = "watchlist"

urlpatterns = [
    path("", views.watchlist_view, name="watchlist"),
    path("add/<int:bike_id>/", views.add_to_watchlist, name="add"),
    path("remove/<int:bike_id>/", views.remove_from_watchlist, name="remove"),
]
