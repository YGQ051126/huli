from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'bed1', 'bed2', 'bed3', 'bed4', 'created_at']
    list_filter = ['created_at']
    search_fields = ['room_number']
    readonly_fields = ['created_at', 'updated_at']