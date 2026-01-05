from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "phone", "location"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded border dark:bg-gray-700"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 rounded border dark:bg-gray-700"
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]

        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 rounded border dark:bg-gray-700",
                "rows": 4
            }),
        }
