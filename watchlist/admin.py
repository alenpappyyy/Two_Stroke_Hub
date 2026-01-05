from django.contrib import admin
from .models import WatchlistItem

@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "bike", "created_at")
