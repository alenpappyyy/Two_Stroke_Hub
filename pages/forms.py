from django import forms
from django.utils import timezone
from datetime import timedelta


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "w-full p-3 rounded bg-gray-800 text-white",
            "placeholder": "Your name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full p-3 rounded bg-gray-800 text-white",
            "placeholder": "Your email"
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "w-full p-3 rounded bg-gray-800 text-white",
            "placeholder": "Subject"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full p-3 rounded bg-gray-800 text-white",
            "rows": 5,
            "placeholder": "Your message"
        })
    )

    # 🔒 Honeypot field (hidden from users)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    # hidden timestamp
    timestamp = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput
    )

    def clean_website(self):
        """Block bots filling hidden field"""
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Bot detected.")
        return ""

    def clean(self):
        """Block instant submissions"""
        cleaned_data = super().clean()
        timestamp = cleaned_data.get("timestamp")

        if timestamp:
            if timezone.now() - timestamp < timedelta(seconds=5):
                raise forms.ValidationError("Form submitted too quickly.")

        return cleaned_data
