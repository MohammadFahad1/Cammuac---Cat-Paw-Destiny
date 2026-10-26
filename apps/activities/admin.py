from django.contrib import admin
from .models import DailyCheckIn


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'lucky_number', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
