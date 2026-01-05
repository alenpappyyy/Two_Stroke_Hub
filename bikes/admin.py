from django.contrib import admin
from .models import Bike, Category

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'seller', 'created_at', 'price']  # all existing fields
    list_filter = ['seller', 'created_at']  # filterable fields
    search_fields = ['name', 'seller__username']  # optional: add search

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # auto-generate slug


