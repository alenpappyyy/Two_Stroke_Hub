from django import forms
from bikes.models import Bike
from parts.models import Part


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = [
            'name',
            'description',
            'price',
            'image',
            'category',
        ]


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'name',
            'short_description',
            'price',
            'image',
            'category',
        ]
