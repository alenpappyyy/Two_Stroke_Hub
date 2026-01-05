from django.urls import path
from .views import (
    blog_detail,
    blog_create, blog_edit,
    blog_delete, blog_dashboard
)
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path("dashboard/", blog_dashboard, name="blog_dashboard"),

    path("create/new/", blog_create, name="blog_create"),
    path("<slug:slug>/", blog_detail, name="blog_detail"),
    path("<slug:slug>/edit/", blog_edit, name="blog_edit"),
    path("<slug:slug>/delete/", blog_delete, name="blog_delete"),
    
]
