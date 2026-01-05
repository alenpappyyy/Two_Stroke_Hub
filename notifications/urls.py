from django.urls import path
from .views import mark_all_read
from . import views


urlpatterns = [
    path("read-all/", mark_all_read, name="read_all"),
    path("", views.notification_list, name="list"),

]
