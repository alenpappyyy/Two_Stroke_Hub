from django import forms
from .models import ServiceBooking

class ServiceBookingForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = ServiceBooking
        fields = ['phone', 'address', 'preferred_date']
