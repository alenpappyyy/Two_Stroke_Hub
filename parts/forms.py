from django import forms
from .models import Part


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['category', 'name', 'description', 'price', 'stock', 'image']
