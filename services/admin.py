from django.contrib import admin
from .models import Booking, Service  # Make sure you import your models

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('client__username', 'service__title', 'status')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'owner', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category', 'owner__username')

