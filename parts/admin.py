from django.contrib import admin
from .models import Part

@admin.register(Part)
class partAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'price')
