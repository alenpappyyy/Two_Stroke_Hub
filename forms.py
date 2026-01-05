from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        (User.ROLE_BUYER, 'Buyer'),
        (User.ROLE_SELLER, 'Seller'),
        (User.ROLE_MECHANIC, 'Mechanic'),
    ], required=True, initial=User.ROLE_BUYER, help_text="Choose buyer/seller/mechanic. Admins must be set by an admin.")

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2", "first_name", "last_name")

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
