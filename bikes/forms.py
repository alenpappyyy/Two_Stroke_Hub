# bikes/forms.py
from django import forms
from .models import Bike

class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['name', 'description', 'price', 'category', 'image']
