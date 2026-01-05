from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from accounts.views import register

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),  
    path("accounts/", include("django.contrib.auth.urls")), 
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path("register/", register, name="register"),

    path("bikes/", include("bikes.urls")),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path("forum/", include("forum.urls")),
    path("services/", include("services.urls")),
    path("community/", include("community.urls")),
    path("support/", include("support.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("orders/", include("orders.urls")),
    path("cart/", include("cart.urls")),
    path('parts/', include('parts.urls')),
    path("", include("pages.urls")),
    path("", home, name="home"),
    path('profile/', include('profiles.urls')),
    path("watchlist/", include("watchlist.urls")),
    path("notifications/", include("notifications.urls")), 
    path("", include(("pages.urls", "pages"), namespace="pages")),


    path("", include(("pages.urls", "pages"), namespace="pages")),
    path("pages/", include(("pages.urls", "pages"), namespace="pages")),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
