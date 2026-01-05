from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("category/<slug:category_slug>/create-thread/", views.create_thread, name="create_thread"),
    path("category/<slug:category_slug>/thread/<slug:thread_slug>/", views.thread_detail, name="thread_detail"),
    path("category/<slug:category_slug>/thread/<slug:thread_slug>/create-post/", views.create_post, name="create_post"),
    path("post/<int:post_id>/reply/<slug:category_slug>/<slug:thread_slug>/", views.create_reply, name="create_reply"),
    path("vote/", views.vote_post, name="vote_post"),
]
