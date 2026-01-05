from django.urls import path
from . import views



app_name = "community"

urlpatterns = [
    path("", views.community_home, name="community"),
    path("blog/", views.blog, name="blog"),
    path("forum/", views.forum, name="forum"),
    path("events/", views.events, name="events"),

]
