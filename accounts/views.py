from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            # Redirect based on role
            if user.role == "buyer":
                return redirect("dashboard:buyer_dashboard")
            elif user.role == "seller":
                return redirect("dashboard:seller_dashboard")
            elif user.role == "mechanic":
                return redirect("dashboard:mechanic_dashboard")
            elif user.role == "admin":
                return redirect("dashboard:admin_dashboard")

            return redirect("dashboard:dashboard") 

    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "buyer")

        # Create user using custom user model
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,     # your custom field
        )

        login(request, user)
        return redirect("dashboard:dashboard")  # change if needed

    return render(request, "accounts/register.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")