from django.contrib import admin
from .models import Service, ServiceBooking, ServiceCategory



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'service',
        'preferred_date',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'service__name')
    actions = ['confirm_bookings', 'complete_bookings']


    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Mark selected as Confirmed"

    def complete_bookings(self, request, queryset):
        queryset.update(status='completed')
    complete_bookings.short_description = "Mark selected as Completed"
